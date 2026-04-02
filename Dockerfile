# Multi-Agent Framework for Semantic Discovery & GraphRAG
# Multi-stage build: dependency layer (cached) + application layer

# ── Stage 1: Dependencies ─────────────────────────────────────────────────────
FROM python:3.12-slim AS deps

WORKDIR /app

# System dependencies for spaCy, sentence-transformers, and scientific libs
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        git \
    && rm -rf /var/lib/apt/lists/*

# Copy only what hatchling needs for metadata + dependency resolution
COPY pyproject.toml README.md ./
COPY src/__init__.py ./src/

RUN pip install --no-cache-dir . \
    && python -m spacy download en_core_web_sm

# ── Stage 2: Application ──────────────────────────────────────────────────────
FROM python:3.12-slim AS app

WORKDIR /app

# Disable output buffering (logs appear immediately in `docker logs`)
# and prevent .pyc files from being written into the image layer
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Runtime-only system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from deps stage
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY tests/fixtures/ ./tests/fixtures/
COPY pyproject.toml README.md ./

# Install the project itself (no deps needed — already copied from stage 1)
RUN pip install --no-cache-dir --no-deps -e .

# Entrypoint script (must be copied before switching user)
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create non-root user; pre-create the HF cache directory owned by appuser.
# With a bind mount (./data/hf_cache), the host directory is owned by the
# current user so Docker will not override ownership on mount.
RUN useradd --create-home --shell /bin/bash appuser \
    && mkdir -p /app/.cache/huggingface \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

ENTRYPOINT ["/entrypoint.sh"]
CMD ["api"]
