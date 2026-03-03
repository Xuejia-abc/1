from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .service import AssistantService

service = AssistantService()


class ApiHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            return self._json(HTTPStatus.OK, {"status": "ok"})

        if parsed.path == "/api/history":
            user_id = parse_qs(parsed.query).get("user_id", [""])[0]
            return self._json(HTTPStatus.OK, {"items": service.get_history(user_id)})

        if parsed.path == "/api/favorites":
            user_id = parse_qs(parsed.query).get("user_id", [""])[0]
            return self._json(HTTPStatus.OK, {"items": service.get_favorites(user_id)})

        self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        data = self._read_json()

        if parsed.path == "/api/recognitions":
            user_id = data.get("user_id", "")
            image_ref = data.get("image_ref", "")
            voice_note = data.get("voice_note")
            if not user_id or not image_ref:
                return self._json(HTTPStatus.BAD_REQUEST, {"error": "user_id_and_image_ref_required"})
            payload = service.recognize(user_id=user_id, image_ref=image_ref, voice_note=voice_note)
            return self._json(HTTPStatus.CREATED, payload)

        if parsed.path == "/api/favorites":
            try:
                payload = service.create_favorite(
                    user_id=data["user_id"],
                    recognition_id=int(data["recognition_id"]),
                    custom_tag=data.get("custom_tag", "未命名收藏"),
                )
            except (KeyError, ValueError):
                return self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid_favorite_payload"})
            return self._json(HTTPStatus.CREATED, payload)

        if parsed.path == "/api/share-cards":
            try:
                payload = service.build_share_card(int(data["recognition_id"]))
            except (KeyError, ValueError):
                return self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid_recognition_id"})
            return self._json(HTTPStatus.OK, payload)

        self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

    def do_PATCH(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if not parsed.path.startswith("/api/favorites/"):
            return self._json(HTTPStatus.NOT_FOUND, {"error": "not_found"})

        favorite_id = parsed.path.rsplit("/", 1)[-1]
        data = self._read_json()
        try:
            payload = service.rename_favorite(int(favorite_id), data["custom_tag"])
        except (KeyError, ValueError):
            return self._json(HTTPStatus.BAD_REQUEST, {"error": "invalid_favorite_id"})
        return self._json(HTTPStatus.OK, payload)

    def log_message(self, format: str, *args) -> None:  # noqa: A003
        return

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    def _json(self, status: HTTPStatus, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), ApiHandler)
    print(f"Server running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
