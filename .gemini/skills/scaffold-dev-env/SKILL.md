---
name: scaffold-dev-env
description: Scaffolds a multi-container development environment using Docker, Dev Containers, and Docker Compose. Use this when the user wants to set up a new project or environment with an application and external technologies (e.g., databases, caches). Supports automated language detection (defaulting to Python with astral-uv), healthcheck validation, GitHub Actions, and VS Code integration.
---

# Scaffold Dev Env

## Overview
This skill automates the creation of a professional-grade, multi-container development environment. It follows best practices for Dev Containers, ensuring a consistent setup across local development, VS Code, and CI/CD.

## Workflow

### 1. Research & Detection
- **Detect Language:** Check if the repository has existing code.
  - If empty and no language specified: Use **Python**.
  - If existing: Detect via files (e.g., `package.json`, `Cargo.toml`, `requirements.txt`).
- **External Tech:** Identify required external services (e.g., PostgreSQL, Redis) from user request or app needs.

### 2. Environment Configuration
- **Python Stack:** If Python is used, always use **astral-uv** for dependency management and **ruff** for linting/formatting.
- **Docker Compose:** Generate `docker-compose.yml` with:
  - App service (pointing to `.devcontainer/Dockerfile`).
  - External service containers with **healthchecks**.
  - **Persistence:** Docker volumes for persistent data.
  - **Secrets:** Use `.env` file; never hardcode passwords.
- **Dev Container:** Generate `.devcontainer/devcontainer.json` with:
  - VS Code extensions: Python, Pylance, Ruff, Docker (including Compose support), and REST Client.
  - Settings to enable **pytest** in the VS Code testing window.
  - Port forwarding for all services.
  - Lifecycle hooks (`postCreateCommand`) to install dependencies.

### 3. Automation & Validation
- **GitHub Actions:** Generate `.github/workflows/test.yml` using the same `docker-compose.yml`.
- **Reset Script:** Generate a Python `reset.py` script to safely teardown (including volumes) and rebuild the environment.
- **API Testing:** Generate `.vscode/api.http` for testing endpoints.
- **Init Scripts:** If the user describes a schema or initial state, generate Python-based initialization scripts.

### 4. Test & Teardown
- **Automated Validation:** After scaffolding, perform a complete "Start -> Test -> Teardown" cycle.
- **pytest:** Ensure a baseline `tests/test_health.py` is created to verify API connectivity.
- **Cleanup:** Always stop and remove the environment after validation to leave the host system clean.

## Templates & Guidelines

Refer to these files for specific implementation details:
- **Docker & Compose:** [references/docker-compose.md](references/docker-compose.md)
- **Dev Container:** [references/devcontainer.md](references/devcontainer.md)
- **Python (uv/ruff):** [references/python.md](references/python.md)
- **Automation (GHA/Reset):** [references/automation.md](references/automation.md)
- **Init & Secrets:** [references/init-scripts.md](references/init-scripts.md)

## Validation Checklist
Before finishing, you MUST verify:
1. `docker compose up -d --build` starts all containers without errors.
2. Healthchecks pass for external services.
3. `.env` file is generated and ignored in `.gitignore`.
4. Dev Container extensions and settings are configured.
5. **pytest** runs successfully within the container (e.g., `docker compose exec -T app pytest`).
6. **Teardown:** `docker compose down -v` successfully removes all containers and volumes.
