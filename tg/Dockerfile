# Pull base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# NOTE: Using Russian text may lead to errors 0, 137
# Output print to the Docker console
ENV PYTHONUNBUFFERED 1

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml pyproject.toml

# Install dependencies
RUN uv sync

# Copy project
COPY . /app

# Run
CMD uv run python app.py
