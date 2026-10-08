"""Receive browser screenshots through a temporary localhost-only form.

Run while collecting Learner Lab evidence, then stop the process. The form
accepts only browser JPEG images and writes only the three named week-1 evidence files.
"""

from base64 import b64decode
from binascii import Error as Base64Error
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs


ROOT = Path(__file__).resolve().parent.parent
TARGETS = {
    "stack": ROOT / "evidence/week-1/02-stack-complete.jpg",
    "network": ROOT / "evidence/week-1/03-network-check.jpg",
    "s3": ROOT / "evidence/week-1/04-s3-private.jpg",
}
JPEG_HEADER = b"\xff\xd8\xff"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"""<!doctype html><meta charset='utf-8'><title>Save Lab evidence</title>
<h1>Save Learner Lab screenshot locally</h1>
<form action='/save' method='post'>
<label>Evidence <select name='name'>
<option value='stack'>Stack</option><option value='network'>Network</option>
<option value='s3'>S3</option></select></label><br>
<label>JPEG base64 <textarea name='png' rows='5' cols='60'></textarea></label><br>
<button type='submit'>Save JPEG</button></form>"""
        self._reply(200, body)

    def do_POST(self):
        if self.path != "/save":
            self._reply(404, b"Not found")
            return
        length = int(self.headers.get("Content-Length", "0"))
        if not 0 < length <= 3_000_000:
            self._reply(413, b"Invalid size")
            return
        fields = parse_qs(self.rfile.read(length).decode("ascii"))
        name = fields.get("name", [""])[0]
        if name not in TARGETS:
            self._reply(400, b"Invalid evidence name")
            return
        try:
            data = b64decode(fields.get("png", [""])[0], validate=True)
        except Base64Error:
            self._reply(400, b"Invalid base64")
            return
        if not data.startswith(JPEG_HEADER):
            self._reply(400, b"JPEG required")
            return
        target = TARGETS[name]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        self._reply(200, f"Saved {target.name} ({len(data)} bytes)".encode())

    def _reply(self, status, body):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 37685), Handler)
    print("Evidence receiver on http://127.0.0.1:37685", flush=True)
    server.serve_forever()
