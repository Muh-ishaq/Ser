from hashlib import sha256
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import secrets
import string


SERVER_DATA_DIR = Path("/serverdata")
FILE_PATH = SERVER_DATA_DIR / "random.txt"
FILE_SIZE = 1024
PORT = 8000


def create_file() -> bytes:
    SERVER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    alphabet = string.ascii_letters + string.digits + " \n"
    data = "".join(secrets.choice(alphabet) for _ in range(FILE_SIZE)).encode("ascii")
    FILE_PATH.write_bytes(data)
    return data


class FileHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path != "/download":
            self.send_error(404, "Use GET /download")
            return

        data = FILE_PATH.read_bytes()
        checksum = sha256(data).hexdigest()

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=us-ascii")
        self.send_header("Content-Disposition", 'attachment; filename="random.txt"')
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Checksum-SHA256", checksum)
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    create_file()
    server = ThreadingHTTPServer(("0.0.0.0", PORT), FileHandler)
    print(f"Serving {FILE_PATH} on port {PORT}", flush=True)
    server.serve_forever()
