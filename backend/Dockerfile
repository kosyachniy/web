# Multi-stage Dockerfile for development and production

# ========================================
# Builder Stage - Install dependencies
# ========================================
FROM python:3.11-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    # --no-install-recommends \
    build-essential \
    # gcc \
    # g++ \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* ./

# # Configure uv for optimal builds
# ENV UV_COMPILE_BYTECODE=1 \
#     UV_LINK_MODE=copy \
#     UV_PYTHON_DOWNLOADS=never

# ========================================
# Development Stage
# ========================================
FROM base as development

# Install dependencies including dev
RUN uv sync --dev

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Development command with hot reload
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ========================================
# Production Builder Stage
# ========================================
FROM base as builder

# Install only production dependencies
# RUN uv sync --no-dev
RUN uv sync --frozen --no-cache

# ========================================
# Production Stage
# ========================================
FROM python:3.11-slim as production

# Install system dependencies for production
RUN apt-get update && apt-get install -y \
    # --no-install-recommends \
    # curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Make sure we use venv
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user
RUN adduser --disabled-password --gecos '' --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Production command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
