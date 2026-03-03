from __future__ import annotations

import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

from life_assistant.server import ApiHandler


def _start_server() -> tuple[ThreadingHTTPServer, int]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), ApiHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, server.server_port


def test_root_page_served() -> None:
    server, port = _start_server()
    try:
        with urlopen(f"http://127.0.0.1:{port}/") as response:
            body = response.read().decode("utf-8")
            assert response.status == 200
            assert "智能生活识别助手" in body
    finally:
        server.shutdown()
        server.server_close()


def test_static_path_traversal_blocked() -> None:
    server, port = _start_server()
    try:
        try:
            urlopen(f"http://127.0.0.1:{port}/static/../server.py")
            assert False, "Expected HTTPError for blocked traversal"
        except HTTPError as err:
            assert err.code == 404
    finally:
        server.shutdown()
        server.server_close()
