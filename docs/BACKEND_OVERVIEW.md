# Backend Overview

## Structure

```
app/
  api/
    router.py          # Mounts versioned routes
    v1/routes/*.py     # Auth, users, posts, websocket
    v1/dependencies.py # Shared dependency factories
  clients/             # External service clients (redis, http, etc.)
  core/                # Config, logging, security, sentry glue
  db/                  # SQLAlchemy engine/session helpers
  models/              # SQLAlchemy ORM models
  schemas/             # Pydantic models for API I/O
  services/            # Business logic (auth, permissions)
  tasks/               # Async background task registry + jobs
  cli.py               # Typer-based CLI utilities
main.py                # FastAPI application factory
```

## Key Concepts

### Configuration
- `app/core/config.py` leverages `pydantic-settings` for env-driven config.
- `settings.setup()` bootstraps DB/Redis connections and background tasks.
- `.env.example` lists required variables; secrets should be injected via runtime env.

### Database Layer
- SQLAlchemy 2.x async ORM with PostgreSQL (asyncpg driver).
- Alembic migrations stored under `app/migrations`; initial revision seeds `users`, `posts`, and login history tables.
- Tests use SQLite (`sqlite+aiosqlite`) via fixtures for lightweight execution.

### Authentication & Authorization
- `AuthService` handles registration, login, refresh, and session snapshots backed by Redis.
- Access tokens are JWT (HS512); refresh tokens stored and validated via Redis TTL keys.
- `permission_required()` dependency enforces RBAC using `PermissionService` and `ROLE_HIERARCHY`.

### Background Tasks
- `AsyncTaskRegistry` supports three paradigms:
  - `@periodic_task`: run at fixed intervals (cron-style).
  - `@event_handler`: respond to domain events (e.g., `user.registered`).
  - `@sequential_task`: process a queue sequentially (no concurrency).
- Jobs register via decorators in `app/tasks/jobs.py`; registry starts during app lifespan.

### Integrations
- `clients/http.py` exposes a base async HTTP client for third-party services plus an example `PaymentsGateway` wrapper.
- Extend by adding provider-specific modules and injecting them into services.

### Observability
- Loguru configured in `core/logging.py` with JSON-friendly format.
- Sentry integration enabled via `SENTRY_DSN`; includes FastAPI + SQLAlchemy instrumentation.
- Background tasks reuse same logging + sentry wiring because they run in-process.

### Testing
- Pytest with asyncio support; fixtures in `tests/conftest.py` provide DB + fake Redis.
- Coverage enforced via `pyproject.toml` `pytest` settings (`--cov=app`).
- Example test `tests/test_auth_service.py` demonstrates service-level assertions.

## Running Locally

```
make install-backend
make dev-backend
```

or via Docker Compose (see `docker-compose.yml`). Uvicorn reload enabled in dev.

## Adding New Modules

1. Create SQLAlchemy models + Pydantic schemas.
2. Generate Alembic migration and apply.
3. Build services and route handlers; wire dependencies.
4. Mirror contract in `frontend/lib/schemas` and update API hooks.
5. Cover with tests and extend docs.
