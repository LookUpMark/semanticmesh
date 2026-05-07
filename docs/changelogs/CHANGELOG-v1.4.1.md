# Changelog — v1.4.1

**Date:** 2026-05-07

## Summary

Patch release — API session logging refactored into per-run subdirectories; Swagger defaults aligned with current environment configuration.

## Changes

### Refactoring

- **API session logs organized into per-run subdirectories** (`src/api/app.py`): Each API session now creates its own directory under `outputs/api/session_YYYYMMDD_HHMMSS/` containing `session.log` and `usage.json`, replacing the previous flat file layout. Simplifies log management and per-session analysis.

### Configuration

- **Swagger defaults aligned with current `.env`** (`src/api/models.py`, `src/config/config.py`): Verified and synchronized all default values in `PipelineConfig`, `CustomAblationRequest`, and `PresetAblationRequest` with the active environment — including model names (`gpt-5.4-nano-2026-03-17`, `gpt-5-nano-2025-08-07`), provider (`openai`), chunking (`256/32`), and feature flags.

### Housekeeping

- **`.gitignore` updated** for new session directory structure (`outputs/api/session_*/`).
