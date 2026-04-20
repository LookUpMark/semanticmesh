# Changelog — v1.0.1

**Date:** 2026-04-17
**Audit Reference:** docs/audits/AUDIT-2026-04-17-171000.md

## Summary

Docker app-containerization removed. Backend API and frontend now run natively (Docker retained only for Neo4j). Five audit findings fixed: port config coupling, inconsistent placeholders, and hardcoded LLM parameters.

## Changes

### Infrastructure

- **Removed Docker app containerization:** Deleted `Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml`, `.dockerignore`, `frontend/.dockerignore`, `docker/entrypoint.sh`, and `docker/` directory. Backend runs via `python -m scripts.serve_api`, frontend via `npm run dev`.
- **Updated `frontend/nginx.conf`:** Replaced Docker DNS resolver (`127.0.0.11`) with envsubst-friendly `$API_HOST`/`$API_PORT` variables (defaults: `localhost:8000`).
- **Updated `scripts/serve_api.py`:** Port default now reads `API_PORT` env var (fallback: 8000).
- **Updated `.env`:** Removed Docker Compose header. Added `.env.example` as the canonical template.

### Configuration

- **Added `llm_request_timeout`** to `AppConfig` / `Settings` (`default=120`). All 4 LLM builders in `model_builders.py` now read from config instead of hardcoded value. Override via `LLM_REQUEST_TIMEOUT` env var.
- **Added `azure_openai_api_version`** to `AppConfig` (`default="2024-11-01-preview"`). Azure builder reads from config instead of hardcoded string. Override via `AZURE_OPENAI_API_VERSION` env var.
- **Standardized Neo4j password placeholder** to `changeme` across `.env.example` and `docs/RUNNING_SERVICES.md`.

### Documentation

- **README.md:** Replaced "Quick Start (Docker)" with native Quick Start (install + `docker run` for Neo4j + `serve_api`).
- **CLAUDE.md:** Updated Neo4j dev command comment to clarify Docker is only for Neo4j.
- **CHANGELOG.md:** Removed Docker containerization entries from v1.0.0 release notes.
- **docs/RUNNING_SERVICES.md:** Removed Docker Issues troubleshooting, updated env setup instructions.
- **docs/draft/REQUIREMENTS.md:** Replaced `.env.docker` references with `.env.example`.
- **docs/draft/ADR.md:** Updated Neo4j deployment note.
- **.gitattributes:** Removed Docker file line-ending rules.

## Files Changed

| Action | File |
|--------|------|
| Deleted | `Dockerfile`, `frontend/Dockerfile`, `docker-compose.yml`, `.dockerignore`, `frontend/.dockerignore`, `docker/entrypoint.sh`, `docker/`, `.env.docker` |
| Added | `.env.example` |
| Modified | `frontend/nginx.conf`, `scripts/serve_api.py`, `src/config/config.py`, `src/config/settings.py`, `src/config/model_builders.py`, `.env`, `.gitattributes`, `.env.example`, `README.md`, `CLAUDE.md`, `CHANGELOG.md`, `docs/RUNNING_SERVICES.md`, `docs/draft/REQUIREMENTS.md`, `docs/draft/ADR.md` |

## Verification

- Unit tests: PASSED (362 tests, 0 failures)
- Regressions: none
