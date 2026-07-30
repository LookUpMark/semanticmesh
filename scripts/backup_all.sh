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

echo "[$(date)] Dumping Neo4j database..."
docker exec semanticmesh-neo4j neo4j-admin database dump neo4j --to-path=/tmp
docker cp semanticmesh-neo4j:/tmp/neo4j.dump ./backups/neo4j_$(date +%Y%m%d_%H%M%S).dump
echo "[$(date)] Neo4j dump complete"

# 2. OWL export (if API is running)
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

# 3. Clean old backups (keep last 7 days)
echo "[$(date)] Cleaning old backups..."
find ./backups -name "neo4j_*.dump" -mtime +7 -delete
find ./backups -name "owl_export_meta.json" -mtime +7 -delete

echo "[$(date)] Backup complete!"
