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

# Resolve the actual Neo4j volume BEFORE compose down (down invalidates project context).
VOLUME=$(docker volume ls --format '{{.Name}}' | grep 'neo4j_data$' | head -1)
if [ -z "$VOLUME" ]; then
    echo "Error: neo4j_data volume not found"
    exit 1
fi

# 1. Stop services (keeps volume)
echo "[$(date)] Stopping services..."
docker compose down

# 2. Stage the chosen backup as neo4j.dump (neo4j-admin load expects <dbname>.dump)
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
cp "$BACKUP_FILE" "$STAGE/neo4j.dump"
# neo4j-admin runs as uid 7474 inside the container — make stage world-readable
chmod -R a+rX "$STAGE"

# 3. Restore into volume via temp container. Volume (rw) at /data, staged dump (ro) at /restore.
echo "[$(date)] Restoring Neo4j backup into volume ($VOLUME)..."
docker run --rm -v "${VOLUME}:/data" -v "${STAGE}:/restore:ro" neo4j:5 \
    neo4j-admin database load neo4j --from-path=/restore --overwrite-destination=true

# 4. Start services
echo "[$(date)] Starting services..."
docker compose up -d

echo "[$(date)] Rollback complete! Neo4j restored from $VERSION."
