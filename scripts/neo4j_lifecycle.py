"""Neo4j Docker lifecycle helpers — start/stop the thesis container.

Usage in notebook (start at top):

    from scripts.neo4j_lifecycle import start_neo4j, stop_neo4j
    start_neo4j()                  # starts / resumes the container

Usage in notebook (stop at bottom, or via atexit):

    stop_neo4j()                   # stops the container cleanly

The container is created on first run and reused afterwards.  Data is
persisted across runs via the named volume ``neo4j-thesis-data``.
"""

from __future__ import annotations

import atexit
import os
import subprocess
import time

# ── Configuration ─────────────────────────────────────────────────────────────

CONTAINER_NAME = os.getenv("NEO4J_CONTAINER_NAME", "neo4j-thesis")
IMAGE = os.getenv("NEO4J_DOCKER_IMAGE", "neo4j:5")
_password = os.getenv("NEO4J_PASSWORD")
if not _password:
    raise SystemExit("NEO4J_PASSWORD env var is required. Set it before running this script.")
NEO4J_AUTH = f"{os.getenv('NEO4J_USER', 'neo4j')}/{_password}"
HTTP_PORT = int(os.getenv("NEO4J_HTTP_PORT", "7474"))
BOLT_PORT = int(os.getenv("NEO4J_BOLT_PORT", "7687"))
VOLUME_NAME = os.getenv("NEO4J_VOLUME_NAME", "neo4j-thesis-data")
STARTUP_TIMEOUT = int(os.getenv("NEO4J_STARTUP_TIMEOUT", "60"))


def _get_neo4j_host() -> str:
    """Parse host from NEO4J_URI, falling back to localhost."""
    uri = os.getenv("NEO4J_URI", "")
    if uri:
        # bolt://host:port or neo4j://host:port
        try:
            import re

            m = re.match(r"(?:bolt|neo4j\+s?s?)://([^:]+)", uri)
            if m:
                return m.group(1)
        except Exception:
            pass
    return "localhost"


def _run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def _container_status() -> str:
    """Return container state string ('running', 'exited', '') if absent."""
    result = _run(
        ["docker", "inspect", "--format", "{{.State.Status}}", CONTAINER_NAME],
        check=False,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _wait_for_bolt(timeout: int = STARTUP_TIMEOUT) -> bool:
    """Poll until Neo4j Bolt port accepts connections or timeout expires."""
    import socket

    host = _get_neo4j_host()
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, BOLT_PORT), timeout=1):
                return True
        except OSError:
            time.sleep(2)
    return False


# ── Public API ────────────────────────────────────────────────────────────────


def start_neo4j(register_stop_atexit: bool = True) -> None:
    """Start (or resume) the Neo4j Docker container.

    - If the container does not exist, creates it with a named volume so
      data survives across notebook runs.
    - If the container is stopped, restarts it.
    - If already running, does nothing.

    Args:
        register_stop_atexit: When True (default), registers ``stop_neo4j``
            as an ``atexit`` handler so the container is stopped when the
            Python interpreter exits (kernel restart / notebook shutdown).
    """
    status = _container_status()

    if status == "running":
        print(f"✅ Neo4j already running  (bolt://{_get_neo4j_host()}:{BOLT_PORT})")
    elif status == "exited":
        print("▶  Resuming stopped Neo4j container …")
        _run(["docker", "start", CONTAINER_NAME])
        _wait_ready()
    else:
        print("🚀 Creating Neo4j container …")
        _run(
            [
                "docker",
                "run",
                "--detach",
                "--name",
                CONTAINER_NAME,
                "-p",
                f"{HTTP_PORT}:{HTTP_PORT}",
                "-p",
                f"{BOLT_PORT}:{BOLT_PORT}",
                "-e",
                f"NEO4J_AUTH={NEO4J_AUTH}",
                "--volume",
                f"{VOLUME_NAME}:/data",
                IMAGE,
            ]
        )
        _wait_ready()

    if register_stop_atexit:
        atexit.register(stop_neo4j)


def _wait_ready() -> None:
    print("⏳ Waiting for Neo4j to be ready …", end="", flush=True)
    if _wait_for_bolt():
        print(f"  ready ✅  (bolt://{_get_neo4j_host()}:{BOLT_PORT})")
    else:
        print(
            f"\n⚠️  Neo4j did not become ready within {STARTUP_TIMEOUT}s — check `docker logs {CONTAINER_NAME}`"
        )


def stop_neo4j() -> None:
    """Stop the Neo4j container (data is preserved in the named volume)."""
    status = _container_status()
    if status == "running":
        print("🛑 Stopping Neo4j container …", end="", flush=True)
        _run(["docker", "stop", CONTAINER_NAME], check=False)
        print("  stopped.")
    else:
        print(
            f"ℹ️  Neo4j container is not running (status: '{status or 'absent'}') — nothing to stop."
        )
