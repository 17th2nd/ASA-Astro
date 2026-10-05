"""Stdlib HTTP server for the ASA-Astro V1 thin slice. No third-party web framework.

    PYTHONPATH=src:. python3 -m app.server            # http://127.0.0.1:8765/

API
  GET  /api/health
  GET  /api/pin                      verified ASA pin (633f837a current-dev pin file)
  GET  /api/objectives               objectives available to evaluate (one per run)
  POST /api/runs  {"objective": slug} run pin → snapshot → ONE objective → receipt
  GET  /api/runs?q=text              list / search persisted runs
  GET  /api/runs/<RCPT-…>            labelled view of one run
  GET  /api/runs/<RCPT-…>/artifacts/<name>   raw artifact (receipt.json, snapshot.json, …)
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import traceback
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import APP_VERSION
from . import pin as pinmod
from . import slice as slicemod

STATIC = Path(__file__).resolve().parent / "static"
MAX_BODY = 4096


class Handler(BaseHTTPRequestHandler):
    server_version = f"asa-astro-app/{APP_VERSION}"

    def log_message(self, fmt, *args):  # quieter default logging
        if not getattr(self.server, "quiet", False):
            super().log_message(fmt, *args)

    def _send(self, status: int, body: bytes, ctype: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, value) -> None:
        self._send(status, (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"), "application/json; charset=utf-8")

    def _error(self, status: int, message: str) -> None:
        self._json(status, {"error": message, "status": status})

    def do_GET(self) -> None:  # noqa: N802
        url = urlparse(self.path)
        parts = [p for p in url.path.split("/") if p]
        try:
            if url.path in ("/", "/index.html"):
                return self._static("index.html")
            if parts[:1] == ["static"] and len(parts) == 2:
                return self._static(parts[1])
            if url.path == "/api/health":
                return self._json(200, {"status": "ok", "app_version": APP_VERSION})
            if url.path == "/api/pin":
                return self._json(200, pinmod.activate())
            if url.path == "/api/objectives":
                return self._json(200, {"objectives": slicemod.list_objectives(), "default": pinmod.app_config()["default_inputs"]["objective"]})
            if url.path == "/api/runs":
                q = parse_qs(url.query).get("q", [""])[0]
                return self._json(200, {"runs": slicemod.list_runs(q), "query": q})
            if parts[:2] == ["api", "runs"] and len(parts) == 3:
                view = slicemod.load_view(parts[2])
                return self._json(200, view) if view else self._error(404, "run not found")
            if parts[:2] == ["api", "runs"] and len(parts) == 5 and parts[3] == "artifacts":
                path = slicemod.artifact_path(parts[2], parts[4])
                if path is None:
                    return self._error(404, "artifact not found")
                ctype = "application/json; charset=utf-8" if path.suffix == ".json" else "text/plain; charset=utf-8"
                return self._send(200, path.read_bytes(), ctype)
            return self._error(404, "not found")
        except pinmod.PinError as exc:
            return self._error(503, f"ASA pin not verified: {exc}")
        except Exception as exc:  # pragma: no cover - surfaced to the client honestly
            traceback.print_exc()
            return self._error(500, f"{type(exc).__name__}: {exc}")

    def do_POST(self) -> None:  # noqa: N802
        url = urlparse(self.path)
        if url.path != "/api/runs":
            return self._error(404, "not found")
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return self._error(413, "request body too large")
        try:
            body = json.loads(self.rfile.read(length) or b"{}") if length else {}
            if not isinstance(body, dict):
                return self._error(400, "body must be a JSON object")
            view = slicemod.run_slice(body.get("objective"))
            return self._json(201 if not view.get("reproduced") else 200, view)
        except json.JSONDecodeError:
            return self._error(400, "invalid JSON")
        except ValueError as exc:
            return self._error(400, str(exc))
        except pinmod.PinError as exc:
            return self._error(503, f"ASA pin not verified: {exc}")
        except Exception as exc:
            traceback.print_exc()
            return self._error(500, f"{type(exc).__name__}: {exc}")

    def _static(self, name: str) -> None:
        path = (STATIC / name).resolve()
        if path.parent != STATIC.resolve() or not path.is_file():
            return self._error(404, "not found")
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype.endswith("javascript"):
            ctype += "; charset=utf-8"
        return self._send(200, path.read_bytes(), ctype)


def make_server(host: str, port: int, quiet: bool = False) -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer((host, port), Handler)
    httpd.quiet = quiet
    return httpd


def main(argv: list[str] | None = None) -> int:
    cfg = pinmod.app_config()
    parser = argparse.ArgumentParser(description="ASA-Astro V1 thin-slice application server")
    parser.add_argument("--host", default=cfg["host"])
    parser.add_argument("--port", type=int, default=cfg["port"])
    args = parser.parse_args(argv)
    pin = pinmod.activate()  # fail fast if the pin does not verify
    httpd = make_server(args.host, args.port)
    print(f"ASA-Astro app {APP_VERSION} on http://{args.host}:{args.port}/  ASA pin {pin['pinned_sha']}  data {slicemod.data_dir()}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
