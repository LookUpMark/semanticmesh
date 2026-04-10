"""Entry point: start the GraphRAG Thesis API server.

Usage:
    python -m scripts.serve_api                      # default: 127.0.0.1:8000
    python -m scripts.serve_api --host 0.0.0.0       # expose to network
    python -m scripts.serve_api --port 9000           # custom port
    python -m scripts.serve_api --reload              # auto-reload on code changes
    python -m scripts.serve_api --workers 2           # multiple workers (no --reload)

Swagger UI:  http://127.0.0.1:8000/docs
ReDoc:       http://127.0.0.1:8000/redoc
OpenAPI:     http://127.0.0.1:8000/openapi.json
"""
from __future__ import annotations

import argparse
import sys


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Start the GraphRAG Thesis API (uvicorn).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind address.")
    parser.add_argument("--port", type=int, default=8000, help="Bind port.")
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload on code changes (development only; incompatible with --workers > 1).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of uvicorn worker processes (ignored when --reload is set).",
    )
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["critical", "error", "warning", "info", "debug", "trace"],
        help="Uvicorn log level.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)

    try:
        import uvicorn
    except ImportError:
        print(
            "uvicorn not found. Install it with:\n"
            '    pip install "uvicorn[standard]"',
            file=sys.stderr,
        )
        sys.exit(1)

    kwargs: dict = {
        "app": "src.api.app:app",
        "host": args.host,
        "port": args.port,
        "log_level": args.log_level,
    }
    if args.reload:
        kwargs["reload"] = True
        kwargs["reload_dirs"] = ["src", "scripts"]
        kwargs["reload_excludes"] = [".venv", "node_modules", "graphify-out", "__pycache__"]
    else:
        kwargs["workers"] = args.workers

    print(f"\n  Swagger UI  →  http://{args.host}:{args.port}/docs")
    print(f"  ReDoc       →  http://{args.host}:{args.port}/redoc")
    print(f"  OpenAPI     →  http://{args.host}:{args.port}/openapi.json\n")

    uvicorn.run(**kwargs)


if __name__ == "__main__":
    main()
