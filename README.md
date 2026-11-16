# Random file server

The server creates a new 1,024-byte ASCII text file at `/serverdata/random.txt`
when its container starts. `GET /download` returns the file and includes its
SHA-256 checksum in the `X-Checksum-SHA256` response header.

## Run

The application has no third-party Python dependencies; see
[`requirements.txt`](./requirements.txt).

From this directory, start the container with Docker Compose:

```sh
docker compose up --build
```

In another terminal, download the file and inspect its checksum header:

```sh
curl -D response-headers.txt -o random.txt http://localhost:8000/download
```

The response headers contain `X-Checksum-SHA256`. Verify the downloaded file
locally with `sha256sum random.txt` (or `Get-FileHash random.txt -Algorithm SHA256`
in PowerShell). The generated file is stored in the Compose-managed `servervol`
volume inside the container.
