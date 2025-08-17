# ========================================
# Builder Stage - Install dependencies
# ========================================
FROM python:3.11-slim AS builder

# Install system dependencies needed for building
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy the entire project structure for dependency resolution
COPY . .

# Configure uv for optimal builds
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

# Install dependencies for all components
RUN cd backend && uv sync --frozen --no-cache && \
    cd ../tg && uv sync --frozen --no-cache && \
    cd ../backend/tests && uv sync --frozen --no-cache

# ========================================
# Final Stage - Runtime image
# ========================================
FROM python:3.11-slim AS final

# Metadata
LABEL maintainer="Alex Poloz <alexypoloz@gmail.com>"
LABEL description="Test suite for the application"
LABEL version="1.0.0"

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd --gid 1000 tester && \
    useradd --uid 1000 --gid tester --shell /bin/bash --create-home tester

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy virtual environments from builder
COPY --from=builder --chown=tester:tester /app/backend/.venv /app/backend/.venv
COPY --from=builder --chown=tester:tester /app/tg/.venv /app/tg/.venv
COPY --from=builder --chown=tester:tester /app/backend/tests/.venv /app/backend/tests/.venv

# Set environment variables for runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Copy application code
COPY --chown=tester:tester . .

# Switch to non-root user
USER tester

# Health check for tests (always healthy since it's ephemeral)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=1 \
    CMD echo "Tests container is healthy" || exit 1

# Default command (can be overridden)
CMD ["echo", "Tests container ready. Run specific test commands."]
