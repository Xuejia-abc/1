from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from life_assistant.server import run_server  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Smart Lifestyle Assistant server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind, default: 0.0.0.0")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind, default: 8000")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only verify startup dependencies and exit",
    )
    args = parser.parse_args()

    if args.check:
        print("startup-check: ok")
        return

    run_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
