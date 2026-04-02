#!/usr/bin/env bash
set -euo pipefail

# ── Wait for Neo4j to accept Bolt connections ─────────────────────────────────
wait_for_neo4j() {
    local uri="${NEO4J_URI:-bolt://neo4j:7687}"
    local host="${uri#bolt://}"
    host="${host%:*}"
    local port="${uri##*:}"
    local retries=0
    local max_retries=60

    echo "[entrypoint] Waiting for Neo4j at ${host}:${port} ..."
    until curl -sf "http://${host}:7474" >/dev/null 2>&1; do
        retries=$((retries + 1))
        if [ "$retries" -ge "$max_retries" ]; then
            echo "[entrypoint] ERROR: Neo4j not reachable after ${max_retries}s" >&2
            exit 1
        fi
        sleep 1
    done
    echo "[entrypoint] Neo4j is ready."
}

# ── Main ──────────────────────────────────────────────────────────────────────
case "${1:-api}" in
    api)
        wait_for_neo4j
        echo "[entrypoint] Starting API server on 0.0.0.0:8000 ..."
        exec python -m scripts.serve_api --host 0.0.0.0 --port 8000
        ;;
    test)
        wait_for_neo4j
        echo "[entrypoint] Running unit tests ..."
        exec pytest tests/unit/ -v
        ;;
    shell)
        exec /bin/bash
        ;;
    *)
        exec "$@"
        ;;
esac
