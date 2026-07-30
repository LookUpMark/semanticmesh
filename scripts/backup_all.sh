#!/bin/bash
set -e

echo "[$(date)] Starting backup..."

# 1. Neo4j dump
echo "[$(date)] Dumping Neo4j database..."
docker exec semanticmesh-neo4j neo4j-admin database dump neo4j --to-path=/tmp
docker cp semanticmesh-neo4j:/tmp/neo4j.dump ./backups/neo4j_$(date +%Y%m%d_%H%M%S).dump
echo "[$(date)] Neo4j dump complete"

# 2. OWL export (if API is running)
if curl -sf http://localhost:8000/health > /dev/null; then
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
