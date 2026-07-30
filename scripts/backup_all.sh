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

# OWL export FIRST — while services are up (no downtime yet)
if curl -s --fail http://localhost:8000/health > /dev/null; then
    echo "[$(date)] Exporting OWL..."
    curl -s -X POST -H "X-API-Key: $API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"include_embeddings": false}' \
        http://localhost:8000/api/v1/demo/kg/owl/export \
        -o ./backups/owl_export_meta.json
    echo "[$(date)] OWL export complete"
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
# neo4j-admin runs as uid 7474 (neo4j) inside the container — relax host perms so it can write
chmod 777 ./backups 2>/dev/null || true
docker run --rm -v "${VOLUME}:/data" -v "$(pwd)/backups:/backups" neo4j:5 \
    neo4j-admin database dump neo4j --to-path=/backups
mv ./backups/neo4j.dump "./backups/neo4j_$(date +%Y%m%d_%H%M%S).dump" 2>/dev/null || true
chmod 755 ./backups 2>/dev/null || true
echo "[$(date)] Neo4j dump complete"

echo "[$(date)] Restarting Neo4j..."
docker compose start neo4j

# 3. Clean old backups (keep last 7 days)
echo "[$(date)] Cleaning old backups..."
find ./backups -name "neo4j_*.dump" -mtime +7 -delete
find ./backups -name "owl_export_meta.json" -mtime +7 -delete

echo "[$(date)] Backup complete!"
