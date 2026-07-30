# Changelog — v1.7.0

**Date:** 2026-07-30
**Type:** Minor — Docker Compose deployment (one-command, CPU + GPU auto-detect)

## Summary

SemanticMesh can now be deployed with a single `docker compose up` on any host (CPU-only or NVIDIA GPU). Adds a `Dockerfile`, a 3-service `docker-compose.yml` (Neo4j + API + nginx), automated backup/rollback scripts, and a Production/SSL path. Zero changes to application source — this is a deployment layer.

## What's new

- **`Dockerfile`** — multi-stage build on `python:3.12-slim`. Builder stage installs deps, runtime stage is minimal with a `/health` HEALTHCHECK.
- **`docker-compose.yml`** — three services:
  - `neo4j:5` with APOC plugin + `cypher-shell` healthcheck + persistent volume.
  - `api` (built from the Dockerfile), depends on Neo4j being healthy, resource limits + `restart: unless-stopped`.
  - `nginx:alpine` reverse proxy (optional, for SSL).
- **GPU auto-detection** — uses `deploy.resources.reservations.devices` (driver: nvidia). Docker allocates the GPU if present, runs CPU-only otherwise. No `runtime: nvidia` hard-failure on CPU hosts.
- **`scripts/backup_all.sh`** — automated backup: OWL export (best-effort, non-fatal) + Neo4j `neo4j-admin` dump (stops the DB for ~10s — Neo4j Community has no online backup) + 7-day retention.
- **`scripts/rollback.sh`** — version-based restore: stages the chosen dump, loads it into the volume via a temp container, restarts the stack. Resolves the project-prefixed volume name dynamically.
- **`nginx.conf`** — reverse proxy with HTTP→HTTPS redirect, ACME challenge path, SSL hardening (TLS 1.2+), WebSocket passthrough, `/health` bypass.
- **`.dockerignore`** — keeps `.env` (live API keys), `.git`, `.venv`, and caches out of the build context.
- **README** — new **Deployment** section: Quick Start, GPU Support, Backup & Restore, Operations, Troubleshooting, and the certbot `--standalone` SSL bootstrap sequence.

## Verification

Real clean-deploy + end-to-end run, following the README quickstart exactly:

```
docker compose up neo4j api -d      # clean start from empty volume
curl localhost:8000/health          # → {"status":"ok"}
# DS01 BEST build (7 tables):
#   build 219.8s → 85 nodes, 94 edges (7 concepts, 7 tables, 7 MAPPED_TO, 7 REFERENCES)
#   GPU auto-detected: reranker loaded on CUDA:0 (not requested, automatic)
#   query Q1: grounded, correct answer on customer_master (grader grounded=True)
```

- **Unit:** 561 tests pass, zero regressions (deployment is config/docs only — no source touched).
- **Backup round-trip:** dump (257 MiB, 36 files) + restore verified.
- **Rollback:** version restore into volume verified end-to-end.

## Review-driven fixes

A whole-feature code review caught and fixed before release:

- **rollback data loss (CRITICAL):** the original script stopped/removed the container, deleted the volume, then targeted the removed container — unrecoverable. Rewritten to stage the dump + restore via a temp container before restart.
- **OWL export 422:** `OwlExportRequest` uses `extra="forbid"`; the script sent `{"include_embeddings": false}`. Fixed to `{}`, made non-fatal on empty graph.
- **API OOM:** memory limit 2G → 8G (BGE-M3 + reranker load lazily, ~4 GB).
- **nginx SSL bootstrap:** documented certbot `--standalone` (nginx can't start before certs exist).
- **No more `chmod 777`** on the backup dir — 2-step volume dump instead.

## Files

- `Dockerfile` — created (multi-stage, healthcheck)
- `docker-compose.yml` — created (neo4j + api + nginx)
- `nginx.conf` — created (reverse proxy + SSL)
- `scripts/backup_all.sh`, `scripts/rollback.sh` — created (executable)
- `.dockerignore` — created
- `README.md` — Deployment section added
- `.gitignore` — ignores backup dumps + certbot dirs
- `data/.gitkeep`, `outputs/.gitkeep`, `backups/.gitkeep` — created
