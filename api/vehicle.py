import json
import os
import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class handler(BaseHTTPRequestHandler):
    def respond(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        registration = parse_qs(
            urlparse(self.path).query
        ).get("registration", [""])[0].strip().upper()

        if not re.fullmatch(r"[A-Z]{2}\d{1,2}[A-Z]{0,3}\d{1,4}", registration):
            return self.respond(400, {
                "success": False,
                "type": "vehicle",
                "error": "Invalid vehicle registration format"
            })

        template = os.getenv("VEHICLE_API_TEMPLATE", "")
        api_key = os.getenv("VEHICLE_API_KEY", "")

        if not template or "{registration}" not in template or not api_key:
            return self.respond(503, {
                "success": False,
                "type": "vehicle",
                "error": "Authorized vehicle provider is not configured"
            })

        if not template.startswith("https://"):
            return self.respond(500, {
                "success": False,
                "error": "Provider must use HTTPS"
            })

        url = template.replace("{registration}", quote(registration, safe=""))
        try:
            req = Request(
                url,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {api_key}"
                }
            )
            with urlopen(req, timeout=8) as response:
                data = json.loads(response.read(256_000).decode("utf-8"))

            return self.respond(200, {
                "success": True,
                "type": "vehicle",
                "registration": registration,
                "data": data
            })
        except HTTPError as exc:
            return self.respond(502, {
                "success": False,
                "error": "Vehicle provider returned an error",
                "provider_status": exc.code
            })
        except (URLError, TimeoutError, OSError, ValueError):
            return self.respond(502, {
                "success": False,
                "error": "Vehicle provider unavailable or returned invalid JSON"
            })
