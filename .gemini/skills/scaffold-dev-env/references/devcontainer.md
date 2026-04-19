# Dev Container Templates

## devcontainer.json Template
```json
{
  "name": "App Dev Container",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "app",
  "workspaceFolder": "/workspace",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff",
        "humao.rest-client"
      ],
      "settings": {
        "python.defaultInterpreterPath": "/usr/local/bin/python",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
          "source.fixAll": "explicit",
          "source.organizeImports": "explicit"
        }
      }
    }
  },
  "forwardPorts": [8000, 5432],
  "postCreateCommand": "bash .devcontainer/setup.sh"
}
```

## Dockerfile Template (Python)
```dockerfile
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# Install astral-uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Set up workspace
WORKDIR /workspace
```

## setup.sh Template
```bash
#!/bin/bash
# Install dependencies using uv
uv sync
```
