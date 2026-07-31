# Stage 1: Build dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY pyproject.toml README.md ./
# Runtime image: install the package only (no dev deps, non-editable).
# ponytail: was `-e ".[dev]"` — pulled pytest/mypy/ruff/testcontainers into the
# 9.84GB runtime image. `.[dev]` dropped, `-e` dropped (prod source is read-only).
RUN pip install --no-cache-dir .

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
