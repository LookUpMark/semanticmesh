#!/bin/bash
set -e

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: ./rollback.sh <version>"
    echo "Example: ./rollback.sh 20260730_143022"
    exit 1
fi

BACKUP_FILE="./backups/neo4j_${VERSION}.dump"

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    echo "Available backups:"
    ls -lh ./backups/neo4j_*.dump 2>/dev/null || echo "  None"
    exit 1
fi

echo "[$(date)] Rolling back to version: $VERSION"

# 1. Stop services
echo "[$(date)] Stopping services..."
docker compose down

# 2. Clear Neo4j volume
echo "[$(date)] Clearing Neo4j volume..."
docker volume rm semanticmesh_neo4j_data 2>/dev/null || true

# 3. Restore backup
echo "[$(date)] Restoring Neo4j backup..."
docker cp $BACKUP_FILE semanticmesh-neo4j:/tmp/neo4j.dump
docker exec semanticmesh-neo4j neo4j-admin database load neo4j --from-path=/tmp/neo4j.dump

# 4. Start services
echo "[$(date)] Starting services..."
docker compose up -d

echo "[$(date)] Rollback complete!"
