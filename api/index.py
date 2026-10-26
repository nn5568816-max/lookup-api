from http.server import BaseHTTPRequestHandler
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({
            "success": True,
            "message": "Python API is running",
            "endpoints": {
                "ifsc": "/api/ifsc?ifsc=SBIN0000001",
                "aadhaar": "/api/aadhaar?id=234567890124",
                "vehicle": "/api/vehicle?registration=HR55AL0051"
            }
        }).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)
