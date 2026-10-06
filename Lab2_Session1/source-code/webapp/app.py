"""Tiny web app used for the Docker / Kubernetes lab (standard library only)."""
import json
import os
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = os.environ.get("APP_VERSION", "1.0")
MESSAGE = os.environ.get("APP_MESSAGE", "Hello from the container!")
COLOR = os.environ.get("APP_COLOR", "#1f6feb")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self._send(200, "application/json", json.dumps({"status": "ok"}))
        elif self.path == "/api":
            self._send(200, "application/json", json.dumps(
                {"message": MESSAGE, "version": VERSION, "pod": socket.gethostname()}))
        else:
            page = (f"<html><body style='font-family:Segoe UI,Arial;background:#f6f8fa;text-align:center;padding-top:80px'>"
                    f"<div style='display:inline-block;background:white;border-top:8px solid {COLOR};padding:30px 60px;"
                    f"box-shadow:0 2px 12px #0003;border-radius:8px'><h1>{MESSAGE}</h1>"
                    f"<h2 style='color:{COLOR}'>Version {VERSION}</h2>"
                    f"<p>Served by container / pod: <b>{socket.gethostname()}</b></p></div></body></html>")
            self._send(200, "text/html", page)

    def _send(self, code, ctype, body):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    print(f"Starting web app v{VERSION} on port 5000", flush=True)
    HTTPServer(("0.0.0.0", 5000), Handler).serve_forever()
