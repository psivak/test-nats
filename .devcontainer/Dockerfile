FROM mcr.microsoft.com/devcontainers/python:3.12

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /workspaces/test-nats

# Install dependencies if pyproject.toml exists
COPY pyproject.toml .
RUN uv sync --frozen || true
