# Automation Templates

## GitHub Actions (.github/workflows/test.yml)
```yaml
name: Test Environment
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Start Environment
        run: docker compose up -d
      - name: Wait for Healthchecks
        run: |
          for i in {1..20}; do
            if [ "$(docker inspect -f '{{.State.Health.Status}}' $(docker compose ps -q db))" == "healthy" ]; then
              echo "Database is healthy"
              exit 0
            fi
            echo "Waiting for database..."
            sleep 5
          done
          echo "Database failed to become healthy"
          exit 1
      - name: Run Tests
        run: docker compose exec -T app pytest
      - name: Shutdown
        run: docker compose down
```

## Reset Script (reset.py)
```python
import subprocess
import os

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def reset():
    print("Resetting dev environment...")
    run("docker compose down -v") # -v removes volumes
    run("docker compose up -d")
    print("Environment reset and fresh seed data applied (if init scripts exist).")

if __name__ == "__main__":
    reset()
```

## API Testing (.vscode/api.http)
```http
### Get Health
GET http://localhost:8000/health

### Get Items
GET http://localhost:8000/items

### Create Item
POST http://localhost:8000/items
Content-Type: application/json

{
    "name": "Test Item",
    "description": "Scaffolded by Gemini CLI"
}
```
