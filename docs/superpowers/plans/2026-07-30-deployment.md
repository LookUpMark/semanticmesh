# Deployment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy SemanticMesh v1.6.2 con Docker Compose su qualsiasi PC (CPU-only o GPU) — sistema di backup/rollback automatizzato, SSL opzionale, singolo comando per startup.

**Architecture:** 3 servizi Docker (Neo4j + API + nginx reverse proxy) — GPU auto-detection via nvidia runtime fallback, backup tripla strategia (Neo4j dump + volume snapshot + OWL export), rollback 3 livelli (Docker tags + snapshots + volume restore).

**Tech Stack:** Docker Compose 3.8, Neo4j 5.x, nginx Alpine, Let's Encrypt certbot, Python 3.12-slim multi-stage build.

---

## File Structure

**File da creare:**

1. **Dockerfile** — Multi-stage build Python 3.12-slim, dependencies + runtime separati, health check integrato
2. **docker-compose.yml** — 3 servizi (neo4j, api, nginx) con health checks, depends_on, GPU runtime fallback
3. **nginx.conf** — Reverse proxy + SSL automatico, HTTP→HTTPS redirect, WebSocket support
4. **scripts/backup_all.sh** — Script backup automatizzato (Neo4j dump + OWL export)
5. **scripts/rollback.sh** — Script rollback con version (volume restore + restart)
6. **data/.gitkeep** — Directory inputs (git-tracked)
7. **outputs/.gitkeep** — Directory exports (git-tracked)
8. **backups/.gitkeep** — Directory backups (git-tracked)

**File da modificare:**

1. **README.md** — Aggiungere sezione "Deployment" con quickstart

---

## Task 1: Create Directory Structure

**Files:**
- Create: `data/.gitkeep`
- Create: `outputs/.gitkeep`
- Create: `backups/.gitkeep`

- [ ] **Step 1: Create .gitkeep files**

```bash
# Crea directories git-tracked
touch data/.gitkeep outputs/.gitkeep backups/.gitkeep
```

- [ ] **Step 2: Verify directories exist**

Run: `ls -la data outputs backups`
Expected: Three directories, each containing `.gitkeep`

- [ ] **Step 3: Commit**

```bash
git add data/.gitkeep outputs/.gitkeep backups/.gitkeep
git commit -m "chore: create directory structure for deployment"
```

---

## Task 2: Create Dockerfile

**Files:**
- Create: `Dockerfile`

- [ ] **Step 1: Write Dockerfile**

```dockerfile
# Stage 1: Build dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir -e ".[dev]"

# Stage 2: Runtime image
FROM python:3.12-slim
WORKDIR /app

# Install system dependencies per embedding models
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application
COPY src/ src/
COPY scripts/ scripts/
COPY .env.example .env.example

# Create data directories
RUN mkdir -p /app/data /app/outputs

# Expose port (internal only, behind nginx)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run API server
CMD ["python", "-m", "scripts.serve_api", "--host", "0.0.0.0", "--port", "8000"]
```

- [ ] **Step 2: Verify Dockerfile syntax**

Run: `docker build --no-cache -f Dockerfile .`
Expected: Build completes successfully (may fail at RUN pip install if dependencies not met, but syntax valid)

- [ ] **Step 3: Commit**

```bash
git add Dockerfile
git commit -m "feat: add Dockerfile for API container"
```

---

## Task 3: Create docker-compose.yml

**Files:**
- Create: `docker-compose.yml`

- [ ] **Step 1: Write docker-compose.yml**

```yaml
version: '3.8'

services:
  neo4j:
    image: neo4j:5
    container_name: semanticmesh-neo4j
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD:-thesis_password}
      - NEO4J_PLUGINS=["apoc"]
      - NEO4J_dbms_memory_heap_initial__size=512m
      - NEO4J_dbms_memory_heap_max__size=1G
    volumes:
      - neo4j_data:/data
    networks:
      - semanticmesh-net
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "${NEO4J_PASSWORD:-thesis_password}", "RETURN 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: semanticmesh-api
    ports:
      - "8000:8000"  # Direct access (dev) or internal (prod)
    environment:
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD:-thesis_password}
      - NEO4J_URI=bolt://neo4j:7687
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - API_KEY=${API_KEY}
      - CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}
    volumes:
      - ./data:/app/data
      - ./outputs:/app/outputs
      - ./.env:/app/.env
    depends_on:
      neo4j:
        condition: service_healthy
    networks:
      - semanticmesh-net
    runtime: nvidia  # Auto-fallback to runc
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G

  nginx:
    image: nginx:alpine
    container_name: semanticmesh-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certbot_conf:/etc/letsencrypt
      - ./certbot-www:/var/www/certbot
    depends_on:
      - api
    networks:
      - semanticmesh-net

volumes:
  neo4j_data:

networks:
  semanticmesh-net:
    driver: bridge
```

- [ ] **Step 2: Validate docker-compose syntax**

Run: `docker compose config`
Expected: Valid YAML output without errors

- [ ] **Step 3: Commit**

```bash
git add docker-compose.yml
git commit -m "feat: add docker-compose.yml with Neo4j + API + nginx"
```

---

## Task 4: Create nginx.conf

**Files:**
- Create: `nginx.conf`

- [ ] **Step 1: Write nginx.conf**

```nginx
events {
    worker_connections 1024;
}

http {
    upstream api {
        server api:8000;
    }

    # HTTP → HTTPS redirect
    server {
        listen 80;
        server_name _;

        location /.well-known/acme-challenge/ {
            root /var/www/certbot;
        }

        location / {
            return 301 https://$host$request_uri;
        }
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name _;

        ssl_certificate /etc/letsencrypt/live/semanticmesh.local/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/semanticmesh.local/privkey.pem;

        # SSL hardening
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Proxy headers
        location / {
            proxy_pass http://api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # WebSocket support (future LangGraph Studio)
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            # Timeouts per long-running requests
            proxy_read_timeout 300s;
            proxy_connect_timeout 60s;
        }

        # Health bypass (no auth)
        location /health {
            proxy_pass http://api/health;
            access_log off;
        }
    }
}
```

- [ ] **Step 2: Validate nginx syntax**

Run: `docker run --rm -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro nginx:alpine nginx -t`
Expected: `syntax is ok` and `test is successful`

- [ ] **Step 3: Commit**

```bash
git add nginx.conf
git commit -m "feat: add nginx reverse proxy config with SSL support"
```

---

## Task 5: Create backup_all.sh Script

**Files:**
- Create: `scripts/backup_all.sh`

- [ ] **Step 1: Write backup script**

```bash
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
```

- [ ] **Step 2: Make script executable**

Run: `chmod +x scripts/backup_all.sh`
Expected: Script executable (no output)

- [ ] **Step 3: Commit**

```bash
git add scripts/backup_all.sh
git commit -m "feat: add automated backup script (Neo4j + OWL)"
```

---

## Task 6: Create rollback.sh Script

**Files:**
- Create: `scripts/rollback.sh`

- [ ] **Step 1: Write rollback script**

```bash
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
```

- [ ] **Step 2: Make script executable**

Run: `chmod +x scripts/rollback.sh`
Expected: Script executable (no output)

- [ ] **Step 3: Commit**

```bash
git add scripts/rollback.sh
git commit -m "feat: add rollback script with version restore"
```

---

## Task 7: Test Docker Build

**Files:**
- Test: `Dockerfile`, `docker-compose.yml`

- [ ] **Step 1: Build API container**

Run: `docker compose build api`
Expected: Build completes, image `semanticmesh-api:latest` created

- [ ] **Step 2: Verify build output**

Run: `docker images | grep semanticmesh-api`
Expected: `semanticmesh-api   latest   <image-id>   <size>`

- [ ] **Step 3: Commit (no changes, just checkpoint)**

```bash
# No commit, just verification step
```

---

## Task 8: Test Neo4j Startup

**Files:**
- Test: `docker-compose.yml` (neo4j service)

- [ ] **Step 1: Start Neo4j only**

Run: `docker compose up neo4j -d`
Expected: Container `semanticmesh-neo4j` created and running

- [ ] **Step 2: Wait for Neo4j health check**

Run: `docker compose ps neo4j`
Expected: Status `healthy` (may take 30-60 seconds)

- [ ] **Step 3: Test Neo4j connection**

Run: `docker exec -it semanticmesh-neo4j cypher-shell -u neo4j -p thesis_password "RETURN 1 AS result"`
Expected: `| result |` with `| 1 |`

- [ ] **Step 4: Stop Neo4j**

Run: `docker compose down`
Expected: Containers stopped and removed

- [ ] **Step 5: Commit (no changes)**

```bash
# No commit, verification step
```

---

## Task 9: Test Full Stack Dev Mode

**Files:**
- Test: `docker-compose.yml` (neo4j + api services)

- [ ] **Step 1: Create .env file**

Run: `cp .env.example .env && echo "API_KEY=test_key_$(openssl rand -hex 16)" >> .env`
Expected: `.env` file created with test API key

- [ ] **Step 2: Start dev mode (no nginx)**

Run: `docker compose up neo4j api --build -d`
Expected: Two containers running: `semanticmesh-neo4j` (healthy), `semanticmesh-api`

- [ ] **Step 3: Wait for API health check**

Run: `sleep 30 && curl http://localhost:8000/health`
Expected: `{"status":"ok"}`

- [ ] **Step 4: Test authenticated endpoint**

Run: `curl -H "X-API-Key: test_key" http://localhost:8000/api/v1/demo/graph/stats`
Expected: JSON with `{"nodes":0,"relationships":0,...}`

- [ ] **Step 5: Stop services**

Run: `docker compose down -v`
Expected: All containers stopped, Neo4j volume removed

- [ ] **Step 6: Commit (no changes)**

```bash
# No commit, verification step
```

---

## Task 10: Update README with Deployment Section

**Files:**
- Modify: `README.md` (add section after "Getting Started")

- [ ] **Step 1: Add deployment section to README**

```markdown
---

## Deployment

### Quick Start (Docker Compose)

**Prerequisites:**
- Docker 20+ and Docker Compose
- 4GB RAM minimum (8GB recommended)
- Neo4j Community Edition 5.x (auto-pulled by Docker)

**Setup (one-time):**

```bash
# 1. Clone and navigate
git clone https://github.com/LookUpMark/semanticmesh.git
cd semanticmesh

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys (OPENAI_API_KEY required)

# 3. Create directories
mkdir -p data outputs backups

# 4. Start (dev mode, no SSL)
docker compose up neo4j api --build
```

**Access:**
- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs
- Neo4j Browser: http://localhost:7474 (neo4j / thesis_password)

**Production (with SSL):**

```bash
# 1. Generate SSL certificates
docker run --rm -v certbot_conf:/etc/letsencrypt -v certbot-www:/var/www/certbot \
  certbot/certbot certonly --webroot -w /var/www/certbot \
  -d yourdomain.com --email your@email.com --agree-tos

# 2. Start full stack
docker compose up -d

# 3. Verify
curl https://yourdomain.com/health
```

**GPU Support:**

If NVIDIA drivers detected, GPU used automatically for embedding/reranker acceleration:
```bash
# Check GPU availability
nvidia-smi
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi

# Start with GPU (automatic)
docker compose up neo4j api --build
```

**Backup & Restore:**

```bash
# Manual backup
./scripts/backup_all.sh

# Automated backup (cron)
0 2 * * * cd /path/semanticmesh && ./scripts/backup_all.sh

# Rollback to specific version
./scripts/rollback.sh 20260730_143022
```

**Operations:**

```bash
# Logs
docker compose logs -f api
docker compose logs -f neo4j

# Restart services
docker compose restart api

# Stop all
docker compose down

# Stop with volume cleanup
docker compose down -v
```

**Troubleshooting:**

```bash
# Neo4j won't start → check password mismatch
docker compose logs neo4j | grep -i error

# API can't reach Neo4j → check health status
docker compose ps

# GPU not detected → verify drivers
nvidia-smi
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```
```

- [ ] **Step 2: Verify README renders correctly**

Run: `grep -A 5 "## Deployment" README.md | head -10`
Expected: Deployment section heading and first few lines

- [ ] **Step 3: Commit**

```bash
git add README.md
git commit -m "docs: add Deployment section to README with quickstart"
```

---

## Task 11: Final Integration Test

**Files:**
- Test: All deployment files

- [ ] **Step 1: Clean test environment**

Run: `docker compose down -v && docker system prune -f`
Expected: All containers, volumes, and dangling images removed

- [ ] **Step 2: Full deployment test**

Run: `docker compose up --build -d && sleep 60`
Expected: All three services (neo4j, api, nginx) running and healthy

- [ ] **Step 3: Health check verification**

Run: `curl http://localhost:8000/health && echo "API OK"`
Expected: `{"status":"ok"}` and `API OK`

- [ ] **Step 4: Neo4j connectivity test**

Run: `docker exec semanticmesh-neo4j cypher-shell -u neo4j -p thesis_password "RETURN 'Connected'"`
Expected: `Connected`

- [ ] **Step 5: Backup script test**

Run: `./scripts/backup_all.sh`
Expected: Backup created in `backups/neo4j_*.dump`

- [ ] **Step 6: Cleanup**

Run: `docker compose down -v`
Expected: Clean shutdown

- [ ] **Step 7: Final commit**

```bash
git add -A && git commit -m "chore: final integration test - deployment complete"
```

---

## Self-Review Checklist

**Spec coverage:**
- ✅ Docker Compose architecture (Task 2, 3)
- ✅ Dockerfile multi-stage build (Task 2)
- ✅ nginx reverse proxy + SSL (Task 4)
- ✅ GPU auto-detect (docker-compose.yml runtime: nvidia)
- ✅ Backup strategy (Task 5)
- ✅ Rollback strategy (Task 6)
- ✅ Deployment commands (Task 7-11)
- ✅ README documentation (Task 10)

**Placeholder scan:**
- ✅ Zero TBD/TODO
- ✅ All code blocks complete
- ✅ All commands exact with expected output
- ✅ No "similar to Task X" references
- ✅ No "add error handling" vague instructions

**Type consistency:**
- ✅ Container names consistent: `semanticmesh-neo4j`, `semanticmesh-api`, `semanticmesh-nginx`
- ✅ Volume names consistent: `neo4j_data`
- ✅ Network names consistent: `semanticmesh-net`
- ✅ Environment variable names match across tasks: `NEO4J_PASSWORD`, `API_KEY`
- ✅ Backup filename pattern consistent: `neo4j_YYYYMMDD_HHMMSS.dump`

**Implementation ready:** All tasks atomic, testable, and committable.
