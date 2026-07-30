# Deployment Design - SemanticMesh

**Date:** 2026-07-30
**Status:** Approved
**Approach:** Docker Compose + GPU Auto-Detection

---

## Goal

Deploy SemanticMesh v1.6.2 con Docker Compose su qualsiasi PC (CPU-only o GPU). Sistema di backup/rollback automatizzato, SSL opzionale, singolo comando per startup.

---

## Architecture Overview

**3 servizi in docker-compose.yml:**

1. **neo4j** — Neo4j 5.x Community Edition
   - Image: `neo4j:5`
   - Ports: 7474 (HTTP), 7687 (Bolt)
   - Volume: `neo4j_data` → persistenza KG
   - Environment: `NEO4J_AUTH`, `NEO4J_PLUGINS`

2. **api** — SemanticMesh FastAPI
   - Build: `Dockerfile` FROM python:3.12-slim
   - Ports: 8000 (internal only)
   - Depends on: `neo4j`
   - GPU support: nvidia runtime (detect + use if available)
   - Environment: tutte le vars da `.env`
   - Volume: `data/` → inputs (docs, DDL), outputs (exports)

3. **nginx** (opzionale) — Reverse proxy + SSL
   - Image: `nginx:alpine`
   - Ports: 80 (HTTP), 443 (HTTPS)
   - Volume: `nginx_config`, `certbot_conf`, `certbot-www`
   - Links → api:8000

**GPU detection strategy:**
- Docker runtime fallback: `nvidia` → `runc`
- Se NVIDIA driver presente, usa GPU automaticamente
- API controlla `CUDA_VISIBLE_DEVICES`, usa GPU per embedding/reranker

---

## Dockerfile API

Multi-stage build, ottimizzato CPU + GPU auto-detect.

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

**GPU support nel compose:**
```yaml
runtime: nvidia  # Fallback to runc if nvidia runtime missing
environment:
  - CUDA_VISIBLE_DEVICES=0  # Auto-detected by Docker
```

**Volumi montati:**
- `./data:/app/data` — inputs (docs, DDL)
- `./outputs:/app/outputs` — exports, bundles
- `.env:/app/.env` — config

---

## docker-compose.yml Completo

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

**Comandi singoli:**
```bash
# Dev mode (no nginx)
docker compose up neo4j api --build

# Production mode (con nginx)
docker compose up --build -d

# Stop + clean
docker compose down -v  # -v rimuove volumi Neo4j
```

---

## nginx Reverse Proxy + SSL

**nginx.conf — Reverse proxy + SSL automatico.**

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

**SSL setup con certbot:**

```bash
# 1. Genera certificati (staging)
docker run --rm -v certbot_conf:/etc/letsencrypt -v certbot-www:/var/www/certbot \
  certbot/certbot certonly --staging --webroot -w /var/www/certbot \
  -d semanticmesh.local --email your@email.com --agree-tos

# 2. Produzione (rimuovi --staging)
docker run --rm -v certbot_conf:/etc/letsencrypt -v certbot-www:/var/www/certbot \
  certbot/certbot certonly --webroot -w /var/www/certbot \
  -d semanticmesh.local --email your@email.com --agree-tos

# 3. Auto-renew (cron)
0 3 * * * docker run --rm -v certbot_conf:/etc/letsencrypt certbot/certbot renew --quiet
```

**Semplificazione dev:** salta SSL, usa solo HTTP su porta 8000 diretto.

---

## Backup Strategy

**3 livelli di backup:**

1. **Neo4j dumps automatici** — Script `backup_neo4j.sh`
   ```bash
   # Dump giornaliero Neo4j
   docker exec semanticmesh-neo4j neo4j-admin database dump neo4j --to-path=/tmp/dump
   docker cp semanticmesh-neo4j:/tmp/dump ./backups/neo4j_$(date +%Y%m%d).dump
   ```
   - Cron: `0 2 * * *` (ogni notte)
   - Rotazione: 7 giorni

2. **Volume snapshot** — Docker volume backup
   ```bash
   docker run --rm -v neo4j_data:/data -v $(pwd)/backups:/backup \
     alpine tar czf /backup/neo4j_volume_$(date +%Y%m%d).tar.gz /data
   ```

3. **OWL export KG** — Backup semantico già implementato
   ```bash
   curl -X POST -H "X-API-Key: $KEY" \
     http://localhost:8000/api/v1/demo/kg/owl/export
   ```
   - Portatile, Protégé-compatible
   - Versioned strategy (auto-snapshot)

**Script unico per tutti:**
```bash
# scripts/backup_all.sh
#!/bin/bash
docker compose exec neo4j neo4j-admin database dump neo4j --to-path=/tmp
docker cp semanticmesh-neo4j:/tmp/neo4j.dump ./backups/
curl -X POST -H "X-API-Key: $API_KEY" http://localhost:8000/api/v1/demo/kg/owl/export
```

**Restore:**
```bash
# Neo4j
docker cp ./backups/neo4j.dump semanticmesh-neo4j:/tmp/
docker exec semanticmesh-neo4j neo4j-admin database load neo4j --from-path=/tmp/neo4j.dump

# OWL
curl -X POST -H "X-API-Key: $KEY" -d '{"strategy":"versioned"}' \
  http://localhost:8000/api/v1/demo/kg/owl/import
```

---

## Rollback Strategy

**3 livelli di rollback:**

1. **Docker Compose rollback** — Versioning immagini
   ```bash
   # Tagga versione stabile
   docker compose build api && docker tag semanticmesh-api:latest semanticmesh-api:v1.6.2

   # Rollback istantaneo
   docker tag semanticmesh-api:v1.6.2 semanticmesh-api:latest
   docker compose up -d api
   ```

2. **Neo4j snapshot restore** — Sistema già implementato
   ```bash
   # Lista snapshot
   curl -H "X-API-Key: $KEY" http://localhost:8000/api/v1/demo/kg/snapshots

   # Restore specifico
   curl -X POST -H "X-API-Key: $KEY" \
     -d '{"snapshot_id":"backup_20260730"}' \
     http://localhost:8000/api/v1/demo/kg/snapshots/restore
   ```

3. **Volume completo restore**
   ```bash
   docker compose down -v
   docker run --rm -v neo4j_data:/data -v $(pwd)/backups:/backup \
     alpine tar xzf /backup/neo4j_volume_20260730.tar.gz -C /
   docker compose up -d
   ```

**Script rollback unificato:**
```bash
# scripts/rollback.sh <version>
#!/bin/bash
# 1. Ferma servizi
docker compose down
# 2. Ripristina volume Neo4j
docker run --rm -v neo4j_data:/data -v ./backups:/backup \
  alpine tar xzf /backup/neo4j_volume_$1.tar.gz -C /
# 3. Riavvia
docker compose up -d
```

**Zero downtime** (nginx health check):
```nginx
upstream api {
    server api:8000 max_fails=3 fail_timeout=30s;
}
```

---

## Deployment Commands + Quickstart

**Setup iniziale (una tantum):**
```bash
# 1. Clone repo
git clone https://github.com/LookUpMark/semanticmesh.git
cd semanticmesh

# 2. Configura environment
cp .env.example .env
# Edit .env con le tue API keys

# 3. Crea directories
mkdir -p data outputs backups certbot_conf certbot-www

# 4. Build + start (dev mode, no SSL)
docker compose up neo4j api --build
```

**Produzione con SSL:**
```bash
# 1. Genera certificati
docker run --rm -v certbot_conf:/etc/letsencrypt -v certbot-www:/var/www/certbot \
  certbot/certbot certonly --webroot -w /var/www/certbot \
  -d yourdomain.com --email your@email.com --agree-tos

# 2. Start completo
docker compose up -d

# 3. Verifica
curl https://yourdomain.com/health
curl -H "X-API-Key: $KEY" https://yourdomain.com/api/v1/demo/graph/stats
```

**Backup automatizzato (cron):**
```bash
# Aggiungi a crontab -e
0 2 * * * cd /path/semanticmesh && ./scripts/backup_all.sh
```

**Comandi operativi:**
```bash
# Logs
docker compose logs -f api          # API logs
docker compose exec api python -m scripts.serve_api --reload  # Dev mode

# Restart singolo servizio
docker compose restart api

# Stop completo
docker compose down

# Stop + pulisci volumi
docker compose down -v
```

**Troubleshooting:**
```bash
# Neo4j non parte → controlla password
docker compose logs neo4j | grep -i error

# API non trova Neo4j → controlla health check
docker compose ps

# GPU non usata → verifica driver
nvidia-smi
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

---

## File da Creare

1. **Dockerfile** — Root del progetto
2. **docker-compose.yml** — Root del progetto
3. **nginx.conf** — Root del progetto (opzionale per SSL)
4. **scripts/backup_all.sh** — Script backup automatizzato
5. **scripts/rollback.sh** — Script rollback con version
6. **data/** — Directory per inputs (vuota, git-tracked)
7. **outputs/** — Directory per exports (vuota, git-tracked)
8. **backups/** — Directory per backups (vuota, git-tracked)

---

## Decisioni Prese

1. **Docker Compose invece di Kubernetes** — SemanticMesh pesante (Neo4j + embedding), K8s overkill per deployment single-host
2. **GPU auto-detect non obbligatoria** — CPU-only funziona, embedding rallentati ma funzionali
3. **nginx opzionale per dev** — `docker compose up neo4j api` per sviluppo veloce
4. **SSL con Let's Encrypt** — Gratis, automatico, standard industria
5. **Backup tripla strategia** — Dump + volume + OWL per massima sicurezza
6. **No CI/CD in prima istanza** — Deploy manuale sufficiente, GitHub Actions opzionale dopo

---

## Prossimi Step

1. Creare file Docker + compose
2. Testare deployment CPU-only
3. Testare GPU auto-detect
4. Setup SSL (opzionale)
5. Testare backup/restore
6. Scrivere docs utente finali (README update)
