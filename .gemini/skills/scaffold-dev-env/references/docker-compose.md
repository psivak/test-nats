# Docker Compose Templates

Use these templates to scaffold multi-container environments with healthchecks and persistence.

## PostgreSQL Template
```yaml
services:
  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
      POSTGRES_DB: ${DB_NAME:-app_db}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-postgres} -d ${DB_NAME:-app_db}"]
      interval: 5s
      timeout: 5s
      retries: 5
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

## Redis Template
```yaml
services:
  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
    ports:
      - "6379:6379"

volumes:
  redis_data:
```

## App Container (Dev Container Integration)
```yaml
services:
  app:
    build:
      context: .
      dockerfile: .devcontainer/Dockerfile
    volumes:
      - ..:/workspace:cached
    command: sleep infinity
    depends_on:
      db:
        condition: service_healthy
```

## Port Forwarding
Always forward relevant service ports:
- PostgreSQL: 5432
- Redis: 6379
- App: 8000, 3000, etc.
