# Build stage
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/home/appuser/.local/bin:${PATH}"

# Create non-root user early
RUN groupadd -r appuser && \
    useradd -r -g appuser -s /bin/bash -d /home/appuser appuser && \
    mkdir -p /home/appuser && \
    chown -R appuser:appuser /home/appuser

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build/

# Copy and install dependencies as non-root user
COPY --chown=appuser:appuser requirements.txt .
USER appuser
RUN pip install --user --no-cache-dir --upgrade pip && \
    pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

# Create non-root user
RUN groupadd -r appuser && \
    useradd -r -g appuser -s /bin/bash -d /home/appuser appuser && \
    mkdir -p /home/appuser && \
    chown -R appuser:appuser /home/appuser

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder --chown=appuser:appuser /home/appuser/.local /home/appuser/.local

WORKDIR /app/

# Copy application files
COPY --chown=appuser:appuser app/ app/
COPY --chown=appuser:appuser alembic/ alembic/
COPY --chown=appuser:appuser alembic.ini .

# Switch to non-root user
USER appuser

# Add security options
EXPOSE 8000
ENV PORT=8000



# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Add security options
STOPSIGNAL SIGTERM

# Add security hardening
RUN mkdir -p /tmp/app && chown -R appuser:appuser /tmp/app
ENV HOME=/home/appuser \
    TMPDIR=/tmp/app

# Drop all capabilities and only add necessary ones
USER appuser:appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]