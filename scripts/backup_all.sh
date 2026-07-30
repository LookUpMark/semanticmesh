#!/bin/bash
set -e

# Cleanup trap for interruption
trap 'echo "[$(date)] Backup interrupted"; exit 1' INT TERM

# Check required directory
if [ ! -d "./backups" ]; then
    echo "Error: ./backups directory does not exist"
    exit 1
fi

echo "[$(date)] Starting backup..."

# 1. Neo4j dump
# Check container is running
if ! docker ps --format "{{.Names}}" | grep -q "semanticmesh-neo4j"; then
    echo "Error: semanticmesh-neo4j container not running"
    exit 1
fi

# OWL export — best-effort semantic backup (non-fatal). Must run while DB is up.
# Empty graph or API/auth issues are warned, not fatal — the Neo4j dump is the critical backup.
if curl -s --fail http://localhost:8000/health > /dev/null; then
    echo "[$(date)] Exporting OWL..."
    # OwlExportRequest has extra="forbid" → empty body only
    HTTP_CODE=$(curl -s -o ./backups/owl_export_meta.json -w "%{http_code}" -X POST \
        -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" -d '{}' \
        http://localhost:8000/api/v1/demo/kg/owl/export)
    if [ "$HTTP_CODE" = "200" ]; then
        echo "[$(date)] OWL export complete"
    else
        echo "[$(date)] OWL export skipped (HTTP $HTTP_CODE — e.g. empty graph). Neo4j dump still runs."
        rm -f ./backups/owl_export_meta.json
    fi
else
    echo "[$(date)] API not running, skipping OWL export"
fi

# Neo4j dump — CE has no online backup, must stop DB briefly.
# ponytail: brief downtime (~10s) per backup. Upgrade to Enterprise for online backup.
echo "[$(date)] Stopping Neo4j for consistent dump..."
docker compose stop neo4j

# Resolve the actual Neo4j volume (project-prefixed) — find it regardless of project name
VOLUME=$(docker volume ls --format '{{.Name}}' | grep 'neo4j_data$' | head -1)
if [ -z "$VOLUME" ]; then
    echo "Error: neo4j_data volume not found"
    docker compose start neo4j
    exit 1
fi

echo "[$(date)] Dumping Neo4j (volume: $VOLUME)..."
# Two-step to avoid chmod 777 on the host backups dir:
#   1. dump into the volume (/data is owned by the neo4j user → writeable)
#   2. copy the dump out to the host backups dir via a root alpine container
docker run --rm --entrypoint bash -v "${VOLUME}:/data" neo4j:5 -c \
    "mkdir -p /data/sm-backup-staging && neo4j-admin database dump neo4j --to-path=/data/sm-backup-staging"
docker run --rm -v "${VOLUME}:/data" -v "$(pwd)/backups:/backups" alpine \
    sh -c "mv /data/sm-backup-staging/neo4j.dump \"/backups/neo4j_$(date +%Y%m%d_%H%M%S).dump\" && rm -rf /data/sm-backup-staging"
echo "[$(date)] Neo4j dump complete"

echo "[$(date)] Restarting Neo4j..."
docker compose start neo4j

# 3. Clean old backups (keep last 7 days)
echo "[$(date)] Cleaning old backups..."
find ./backups -name "neo4j_*.dump" -mtime +7 -delete
find ./backups -name "owl_export_meta.json" -mtime +7 -delete

echo "[$(date)] Backup complete!"
