
import json
import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class handler(BaseHTTPRequestHandler):
    def respond(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        value = parse_qs(urlparse(self.path).query).get("id", [""])[0]
        digits = re.sub(r"[\s-]", "", value)

        if not re.fullmatch(r"\d{12}", digits):
            return self.respond(400, {
                "success": False,
                "type": "aadhaar",
                "error": "Provide a 12-digit Aadhaar number"
            })

        masked = "XXXX-XXXX-" + digits[-4:]

        return self.respond(200, {
            "success": True,
            "type": "aadhaar",
            "verified": False,
            "message": "Format checked only; identity not verified",
            "aadhaar": masked
        })
