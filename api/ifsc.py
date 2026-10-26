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
        code = parse_qs(urlparse(self.path).query).get("ifsc", [""])[0]
        code = code.strip().upper()

        if not re.fullmatch(r"[A-Z]{4}0[A-Z0-9]{6}", code):
            return self.respond(400, {
                "success": False,
                "error": "Invalid IFSC format"
            })

        template = os.getenv(
            "IFSC_API_TEMPLATE",
            "https://priyanshuexploits.vercel.app/api/ifsc/{ifsc}?format=text"
        )
        if not template.startswith("https://") or "{ifsc}" not in template:
            return self.respond(503, {
                "success": False,
                "error": "IFSC provider URL is not configured correctly"
            })

        url = template.replace("{ifsc}", quote(code, safe=""))
        try:
            req = Request(url, headers={"Accept": "application/json, text/plain"})
            with urlopen(req, timeout=8) as response:
                raw = response.read(256_000).decode("utf-8", errors="replace")
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = {"raw": raw.strip()}

            return self.respond(200, {
                "success": True,
                "type": "ifsc",
                "ifsc": code,
                "data": data
            })
        except HTTPError as exc:
            return self.respond(502, {
                "success": False,
                "error": "IFSC provider returned an error",
                "provider_status": exc.code
            })
        except (URLError, TimeoutError, OSError):
            return self.respond(502, {
                "success": False,
                "error": "IFSC provider unavailable"
            })
