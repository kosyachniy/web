# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Full-stack web application with Python FastAPI backend, Next.js frontend, and Telegram bot. The application uses Docker containers for deployment and includes monitoring via Prometheus/Grafana.

---

## Golden Rules for Claude
- **Frontend Development**: Follow the **Frontend Development Flow** below for ALL frontend code changes
- **Minimal, focused diffs**: change only what's necessary; keep PRs small (<300 LOC) and self-contained
- **Follow FSD Architecture**: respect Feature-Sliced Design layers and import rules (see *Frontend Architecture*)
- **Never hard-code secrets** or credentials; never read or write `.env`, `secrets/`, or CI secrets
- **Use toasts/popups for feedback**: errors/warnings/success/info should use app toasts/dialogs, not `alert()` or raw text
- **Centralized icon management**: ALL icons MUST be imported from `shared/ui/icons.tsx` file, never directly from `react-icons`
- **React-icons priority system**: use `react-icons` with priority order: 1. `fa6` (Font Awesome 6), 2. `bi` (Bootstrap Icons), 3. `hi` (Heroicons). Never use inline SVG
- **Special symbols vs icons**: use Unicode symbols (©, ®, ™) as text characters, not icons with backgrounds
- **Accessibility first**: proper aria labels/roles, focus states, keyboard nav; no color-only affordances
- **Ask before destructive or external actions** (network, DB migrations, Docker, `git push`, etc.)

---

## Test-Driven Development Workflow ⚠️ **MANDATORY**

**Every feature implementation MUST follow this exact sequence:**

### **1. API Tests First** → **Define Contracts & Edge Cases**
- ✅ **Write comprehensive API tests** covering ALL endpoints, methods, and data flows
- ✅ **Cover ALL edge cases**: invalid data, auth failures, rate limits, database errors, network timeouts
- ✅ **Test request/response models** with boundary values, missing fields, type mismatches
- ✅ **Mock external dependencies** (database, Redis, external APIs) in tests
- ✅ **Use pytest with async support** for FastAPI endpoint testing
- ✅ **Test authentication & authorization** for all protected endpoints
- ✅ **Test pagination, filtering, sorting** for list endpoints
- ✅ **Test error responses** match RFC 7807 Problem Details format
- ❌ **NEVER start backend implementation** without comprehensive API tests

### **2. Backend Implementation** → **Satisfy Tests & Generate Clean OpenAPI**
- ✅ **Implement backend logic** to make ALL tests pass
- ✅ **Follow FastAPI 2025 best practices** with async/await, Pydantic v2, structured logging
- ✅ **Use proper Pydantic field descriptions** and examples for clean OpenAPI generation
- ✅ **Specify response_model** in all FastAPI decorators for accurate schema generation
- ✅ **Add OpenAPI tags** for logical endpoint grouping
- ✅ **Handle ALL error cases** tested in step 1 with proper HTTP status codes
- ✅ **Run `make unit-test`** to ensure all API tests pass before proceeding
- ❌ **NEVER proceed to schema generation** until ALL backend tests are green

### **3. TypeScript Schema Generation** → **Type-Safe Frontend Integration**
- ✅ **Generate TypeScript schemas**: `cd frontend && npm run generate-schemas`
- ✅ **Verify schema generation** produces clean, accurate types from OpenAPI spec
- ✅ **Check generated schemas** in `frontend/src/generated/api/schemas.ts`
- ✅ **Validate field descriptions** and examples appear correctly in generated types
- ✅ **Ensure request/response types** match exactly with backend Pydantic models
- ❌ **NEVER write manual API types** - always use generated schemas

### **4. Frontend Implementation** → **Type-Safe UI Components**
- ✅ **Import ALL types** from `@/generated/api/schemas` - never create manual types
- ✅ **Follow Frontend Development Flow** (6-step systematic process above)
- ✅ **Use generated schemas** for API calls, form validation, Redux state
- ✅ **Implement error handling** with toast notifications using generated error types
- ✅ **Test type safety** - TypeScript compiler should catch any API contract mismatches
- ✅ **Handle loading states** and edge cases from backend API behavior
- ❌ **NEVER hardcode API types** or request/response structures

### **5. Frontend Tests** → **UI & Integration Testing**
- ✅ **Write component tests** for all UI components using generated types
- ✅ **Test ALL user interactions**: clicks, form submissions, navigation, state changes
- ✅ **Test error handling**: network errors, validation failures, auth timeouts
- ✅ **Test edge cases**: empty states, loading states, pagination boundaries
- ✅ **Test responsive behavior**: desktop, tablet, mobile viewports
- ✅ **Test accessibility**: keyboard navigation, screen readers, focus management
- ✅ **Test i18n**: all supported languages, text overflow, RTL layouts
- ✅ **Mock API calls** using generated schemas for predictable test data
- ✅ **Run `make test-web`** to ensure all frontend tests pass
- ❌ **NEVER skip edge case testing** - they're caught in API tests, so UI must handle them

### **TDD Workflow Validation Checklist**
Before considering any feature complete, verify:
1. ✅ API tests cover 100% of endpoints and edge cases (`make unit-test` passes)
2. ✅ Backend implementation satisfies all API tests (all tests green)
3. ✅ OpenAPI spec generates clean, accurate TypeScript schemas
4. ✅ Frontend uses ONLY generated types (no manual API types)
5. ✅ Frontend handles ALL error cases tested in API tests
6. ✅ Frontend tests cover ALL user interactions and edge cases (`make test-web` passes)
7. ✅ Full integration test: API → Schema Generation → Frontend → UI Tests

### **Benefits of This Workflow:**
- **Contract-First Development**: API contracts defined upfront prevent integration issues
- **Comprehensive Coverage**: Edge cases identified early, tested throughout stack
- **Type Safety**: Generated schemas ensure frontend/backend always stay in sync
- **Quality Assurance**: No feature ships without thorough testing at every layer
- **Maintainability**: Changes to API automatically update frontend types and tests
- **Team Coordination**: Clear contracts enable parallel frontend/backend development

**⚠️ CRITICAL: This workflow is MANDATORY for ALL feature development. Never skip steps or proceed to next step with failing tests.**

---

## Backend
### Coding Flow Rules
#### 0) Core Principles (do not violate)

1. **Ports & Adapters.**
   Domain knows **only** interfaces in `app/domain/ports/*`. All IO (DB, HTTP, broker, cache) lives in `app/adapters/*`.
2. **Three data shapes (strict):**
   **API DTOs** → `app/api/schemas/*` (Pydantic request/response).
   **Domain Entities** → `app/domain/entities/*` (business state & invariants, no IO).
   **Persistence Models** → `app/adapters/db/*/models/*` (ORM/collections, physical storage).
3. **Async‑first.** `async def` everywhere (FastAPI, SQLAlchemy 2.0 async, Motor, httpx, redis.asyncio).
4. **Transactions via UoW.** Services use `UnitOfWorkPort`. **Commit first, then side‑effects** (enqueue job / publish event) — never before.
5. **HTTP layer is thin.** Routes validate DTOs and call domain services. No business logic or SQL in endpoints.
6. **Background work is decoupled.**
   Jobs → `app/workers/jobs/*`; Consumers → `app/workers/consumers/*`; Schedules → `app/workers/schedules.py`.
7. **Events are optional.**
   One light reaction → enqueue job right after commit.
   Multiple/independent reactions → publish a typed event (`app/events/*`).

---

#### 1) Repository Map (what goes where)

```
backend/
│
├── .gitignore                     # Git ignore rules
├── pyproject.toml                 # Single source of truth for deps/tools, UV package manager, async deps; scripts; Ruff config can live here
├── uv.lock                        # Dependency lock file
├── Dockerfile                     # Containerization: Multi-stage container
├── .dockerignore                  # Containerization: Docker ignore rules
│
├── app/                           # Main application code
│   ├── main.py                    # FastAPI application factory; mounts routers/middlewares; lifespan wiring
│   │
│   ├── core/                      # Core application configuration; App-level bootstrapping & cross-cutting concerns
│   │   ├── config.py              # Pydantic Settings (centralized configuration); feature flags select adapters (DB/Broker/Tasks)
│   │   ├── lifespan.py            # Application startup/shutdown events: DB clients, Redis, broker conn, httpx client, limiter
│   │   ├── security.py            # JWT issue/verify, password hashing, authentication
│   │   ├── logging.py             # Loguru configuration + std logging intercept + correlation ID; JSON-friendly; request-id field
│   │   ├── rate_limit.py          # Rate limiting setup
│   │   ├── cors.py                # CORSMiddleware config (env-based allowlist)
│   │   └── di.py                  # Dependency providers: bind domain Ports → concrete Adapters by env
│   │
│   ├── middleware/
│   │   └── request_id.py          # Global request-id; attach in main.py
│   │
│   ├── domain/                    # Pure business layer (no FastAPI/DB specifics)
│   │   ├── entities/              # Layer 3: Domain entities (dataclass/Pydantic for domain)
│   │   │   └── audit_log.py
│   │   ├── ports/                 # Layer 4: Domain Ports; Interfaces (hexagonal ports)
│   │   │   ├── user_repo.py       # UserRepository: user-specific queries
│   │   │   ├── session.py         # SessionRepository: session management
│   │   │   ├── audit.py           # AuditRepository: audit trail operations
│   │   │   ├── uow.py             # Unit of Work pattern for transactions: begin/commit/rollback + repo accessors
│   │   │   ├── cache.py           # CachePort
│   │   │   └── message_broker.py  # MessageBrokerPort: publish/subscribe
│   │   └── services/              # Layer 5: Business Logic Services; Business use-cases; orchestrate via Ports/UoW
│   │       ├── auth_service.py    # Authentication logic (register, login, refresh)
│   │       ├── user_service.py    # User management logic
│   │       ├── session_service.py # Session management logic
│   │       ├── audit_service.py   # Audit trail logic
│   │       ├── notification_service.py # Notification sending logic
│   │       └── integration_service.py # External API integration logic
│   │
│   ├── api/                       # Layer 6: HTTP Interface (kept flat for fast dev; can be moved under presentation/ later)
│   │   ├── router.py              # Main router that includes all sub-routers
│   │   ├── errors.py              # Global exception handlers (Problem+JSON)
│   │   ├── health.py              # Liveness/readiness; DB/broker checks (usually unversioned)
│   │   │
│   │   ├── schemas/               # Layer 2: API Schemas (Pydantic DTOs (API contracts)) — NOT ORM, NOT domain entities
│   │   │   ├── base.py            # Base schemas with common patterns
│   │   │   ├── auth.py            # LoginRequest, TokenResponse, RefreshToken
│   │   │   │── user.py            # UserCreate, UserRead, UserUpdate
│   │   │   │── responses.py       # Standard API response schemas
│   │   │   │── pagination.py      # Pagination schemas
│   │   │   └── filters.py         # Filter and search schemas
│   │   │
│   │   ├── deps/                  # API dependencies; Request-scoped DI helpers
│   │   │   ├── uow.py             # get_uow(): UnitOfWorkPort per request
│   │   │   ├── broker.py          # get_broker(): MessageBrokerPort
│   │   │   ├── cache.py           # get_cache(): CachePort
│   │   │   ├── http.py            # get_http_client(): shared httpx.AsyncClient
│   │   │   └── auth.py            # Authentication dependencies
│   │   │
│   │   ├── middleware/            # HTTP middleware
│   │   │   ├── auth.py            # Authentication middleware
│   │   │   ├── cors.py            # CORS middleware setup
│   │   │   ├── rate_limit.py      # Rate limiting middleware
│   │   │   ├── request_id.py      # Request ID correlation middleware
│   │   │   └── logging.py         # Request/response logging middleware
│   │   │
│   │   └── v1/                    # API version 1
│   │       ├── router.py          # Versioned API root
│   │       ├── base.py
│   │       ├── auth.py            # Authentication endpoints (/auth/*)
│   │       ├── users.py           # User management endpoints (/users/*)
│   │       └── health.py          # Health check endpoints (/health/*)
│   │
│   ├── websocket/                 # WS interface (separate transport, same domain services)
│   │   ├── connection_manager.py  # WebSocket connection management
│   │   ├── handlers.py            # WebSocket message handlers
│   │   └── auth.py                # WebSocket authentication
│   │
│   ├── adapters/                  # Infrastructure Adapters; Tech-specific implementations of ports (replaceable)
│   │   ├── database/              # Database implementations
│   │   │   ├── postgres/          # PostgreSQL implementation; SQLAlchemy 2.0 asyncio + asyncpg
│   │   │   │   ├── engine.py      # create_async_engine + sessionmaker
│   │   │   │   ├── models/        # Layer 1: Database Models; Physical storage models (ORM); NOT API schemas
│   │   │   │   │   ├── base.py    # Base model with common fields (id, created_at, updated_at)
│   │   │   │   │   ├── user.py    # User model (Beanie Document / SQLAlchemy)
│   │   │   │   │   ├── session.py # User sessions model
│   │   │   │   │   ├── audit.py   # Audit trail model
│   │   │   │   │   └── tenant.py  # Multi-tenancy model (if needed)
│   │   │   │   ├── repositories/
│   │   │   │   │   └── user_repo.py # implements UserRepoPort using AsyncSession
│   │   │   │   └── uow.py         # PostgresUnitOfWork wrapping AsyncSession transactions
│   │   │   └── mongo/             # MongoDB implementation; Motor (async MongoDB)
│   │   │       ├── client.py      # Motor client/db init; indexes
│   │   │       ├── repositories/
│   │   │       │   └── user_repo.py # implements UserRepoPort via collections
│   │   │       └── uow.py         # MongoUnitOfWork (client session/transactions or no-op fallback)
│   │   ├── cache/                 # Caching implementations
│   │   │   ├── redis.py           # RedisCache implements CachePort (redis.asyncio)
│   │   │   └── memory.py          # In-memory cache for testing
│   │   ├── broker/                # Message brokers (callbacks/events), not task runners
│   │   │   ├── redis_broker.py    # Simple Redis pub/sub
│   │   │   └── rabbitmq/
│   │   │       ├── connection.py  # aio-pika robust connection/channel; declare exchanges/queues
│   │   │       └── broker.py      # implements MessageBrokerPort (publish/consume with ack/retry)
│   │   ├── storage/               # File storage implementations
│   │   │   ├── __init__.py
│   │   │   ├── local.py           # Local file storage
│   │   │   └── s3.py              # AWS S3 storage
│   │   │
│   │   └── external/              # External API clients
│   │       ├── __init__.py
│   │       ├── base_client.py     # Base HTTP client with retry/circuit breaker
│   │       ├── payment/           # Payment gateway clients
│   │       │   ├── __init__.py
│   │       │   ├── stripe.py      # Stripe API client
│   │       │   ├── paypal.py      # PayPal API client
│   │       │   └── models.py      # Payment models
│   │       └── notification/      # Notification service clients
│   │           ├── __init__.py
│   │           ├── email.py       # Email service (SendGrid, SES)
│   │           ├── sms.py         # SMS service (Twilio)
│   │           └── push.py        # Push notifications
│   │
│   ├── jobs/                      # Background Job Processing; Tool-agnostic background execution & consumers
│   │   ├── scheduled/             # Scheduled jobs (cron-like)
│   │   └── callbacks/             # Event-driven jobs
│   │
│   ├── events/                         # Typed contracts for cross-process communication
│   │   ├── schemas.py                  # Pydantic models for event payloads (e.g., UserCreated)
│   │   └── topics.py                   # Topic/route-key constants
│   │
│   ├── utils/                     # Utility Functions; Small, generic helpers (keep tidy; feature-specific utils live with features)
│   │   ├── __init__.py
│   │   ├── validators.py          # Custom validation functions
│   │   ├── formatting.py          # Data formatting utilities
│   │   ├── crypto.py              # Cryptographic utilities
│   │   ├── time.py                # Date/time utilities
│   │   ├── pagination.py          # Pagination helpers
│   │   └── decorators.py          # Utility decorators (retry, cache, etc.)
│   │
│   └── monitoring/                # Observability (optional for advanced setups)
│       ├── __init__.py
│       ├── metrics.py             # Custom metrics collection; Prometheus instrumentation (/metrics)
│       ├── tracing.py             # Distributed tracing setup; OpenTelemetry setup; httpx/broker instrumentation
│       └── health.py              # Health check implementations
│
├── tests/                         # Test Suite
│   ├── __init__.py
│   ├── conftest.py                # Pytest configuration and fixtures
│   │
│   ├── fixtures/                  # Test data fixtures
│   │   ├── __init__.py
│   │   ├── database.py            # Database fixtures
│   │   ├── auth.py                # Authentication fixtures
│   │   └── external_services.py   # External service mocks
│   │
│   ├── unit/                      # Unit tests (services, repositories)
│   │   ├── __init__.py
│   │   ├── services/
│   │   │   ├── test_auth_service.py
│   │   │   ├── test_user_service.py
│   │   │   └── test_notification_service.py
│   │   │
│   │   ├── repositories/
│   │   │   ├── test_user_repository.py
│   │   │   └── test_session_repository.py
│   │   │
│   │   └── utils/
│   │       ├── test_validators.py
│   │       └── test_crypto.py
│   │
│   ├── integration/               # Integration tests (database, external APIs)
│   │   ├── __init__.py
│   │   ├── test_database.py       # Database integration tests
│   │   ├── test_cache.py          # Cache integration tests
│   │   ├── test_message_broker.py # Message broker tests
│   │   └── test_external_apis.py  # External API tests
│   │
│   ├── api/                       # API endpoint tests
│   │   ├── __init__.py
│   │   ├── test_auth.py           # Authentication endpoint tests
│   │   ├── test_users.py          # User endpoint tests
│   │   ├── test_health.py         # Health check tests
│   │   └── test_webhooks.py       # Webhook tests
│   │
│   ├── e2e/                       # End-to-end tests
│   │   ├── __init__.py
│   │   ├── test_user_journey.py   # Complete user workflows
│   │   ├── test_payment_flow.py   # Payment processing flow
│   │   └── test_notification_flow.py # Notification delivery
│   │
│   └── performance/               # Performance tests (optional)
│       ├── __init__.py
│       ├── test_load.py           # Load testing
│       └── test_concurrency.py    # Concurrency testing
│
├── scripts/                       # Utility Scripts
│   ├── migrate.py                 # Run database migrations
│   ├── seed_data.py               # Seed initial data
│   ├── backup_db.py               # Database backup script
│   ├── restore_db.py              # Database restore script
│   └── health_check.py            # Health check script for monitoring
│
├── docs/                          # Documentation
│   ├── README.md                  # Main documentation
│   ├── CONTRIBUTING.md            # Contribution guidelines
│   ├── DEPLOYMENT.md              # Deployment instructions
│   │
│   ├── api/                       # API documentation
│   │   ├── openapi.json           # Generated OpenAPI specification
│   │   └── examples/              # API usage examples
│   │
│   ├── architecture/              # Architecture documentation
│   │   ├── overview.md            # System overview
│   │   ├── database_design.md     # Database schema documentation
│   │   ├── api_design.md          # API design principles
│   │   └── security.md            # Security implementation
│   │
│   ├── operations/                # Runbooks: worker, consumers, migrations, scaling
│   │
│   └── guides/                    # Developer guides
│       ├── getting_started.md     # Quick start guide
│       ├── testing.md             # Testing guide
│       ├── deployment.md          # Deployment guide
│       └── troubleshooting.md     # Common issues and solutions
│
└── db/                            # Database tooling and migrations
    ├── alembic.ini                # Alembic configuration for PostgreSQL migrations
    └── migrations/                # Database migrations
        ├── env.py                 # Alembic environment configuration
        ├── versions/              # Migration version files
        │   ├── 001_*.py           # Migration scripts
        │   └── 002_*.py
        ├── CHEATSHEET.md          # Migration command reference
        ├── MIGRATION_SUMMARY.md   # Migration documentation
        └── RESET_GUIDE.md         # Database reset instructions
```

---

#### 2) Naming & Style

* **Modules**: `snake_case.py`. **Classes**: `CamelCase`. **Functions/vars**: `snake_case`.
* Mandatory **type hints**; `from __future__ import annotations` allowed.
* **Imports**: stdlib → third‑party → internal (absolute imports).
* **Pydantic v2** (`ConfigDict`, `from_attributes=True` for read models).
* **SQLAlchemy 2.0**: `AsyncSession` only, one per request/UoW.
* **Logging**: Loguru via `core/logging.py`; every log line should include request‑id.
* **HTTPX**: use the shared client from DI; set sensible `Timeout` & `Limits`.
* **Redis**: `redis.asyncio` only.
* **Security**: JWT in `core/security.py`, bcrypt for passwords.
* **Forbidden**: business logic inside adapters/routes/jobs — it belongs in domain services.

---

#### 3) Recipes — how to code (for AI & humans)

##### A) New entity (example: **Post**)

**1. Domain**

* `app/domain/entities/post.py` — fields & methods (`publish`, `edit`, `archive`) with no IO.
* `app/domain/ports/post_repo.py` — repository interface:

```python
class PostRepoPort(Protocol):
    async def get(self, post_id: UUID) -> Post | None: ...
    async def create(self, post: Post) -> Post: ...
    async def update(self, post: Post) -> None: ...
    async def list_by_author(self, author_id: UUID, limit: int, cursor: str | None): ...
```

* `app/domain/services/post_service.py` — use‑cases:

```python
async def create_post(dto: PostCreateDTO, uow: UnitOfWorkPort) -> Post:
    post = Post(...)
    await uow.posts.create(post)
    await uow.commit()
    return post

async def publish_post(post_id: UUID, uow: UnitOfWorkPort, jobs: AsyncJobsPort):
    post = await uow.posts.get(post_id)
    post.publish()
    await uow.posts.update(post)
    await uow.commit()                    # 1) commit
    await jobs.post_published(post.id)    # 2) side-effect (or publish event)
```

**2. API (DTO + routes)**

* `app/api/schemas/post.py` → `PostCreate`, `PostUpdate`, `PostRead`.
* `app/api/v1/posts.py` → routes call services; no SQL here.

**3. Persistence**

* **Postgres**:
  `app/adapters/db/postgres/models/post.py` (ORM + indexes),
  `app/adapters/db/postgres/repositories/post_repo.py` (implements `PostRepoPort`),
  migration in `db/migrations/versions/*_add_post.py`.
* **Mongo**:
  `app/adapters/db/mongo/repositories/post_repo.py` (collections + indexes).

**4. Background & Events (if needed)**

* `app/workers/jobs/posts.py` (e.g., `send_post_published_email`).
* `app/workers/consumers/post_events.py` — if publishing `PostPublished`.
* `app/events/schemas.py` — add `PostPublished` (optional).

**5. Tests**

* Unit: `test_post_service.py` (ports mocked).
* Integration: repo tests (PG/Mongo).
* E2E: `POST /posts` → `POST /posts/{id}/publish`.

**Checklist DoR/DoD**

* [ ] Domain does **not** import adapters/FastAPI.
* [ ] Repo implemented for selected DB and bound in DI.
* [ ] Migrations exist & apply cleanly.
* [ ] DTOs match OpenAPI; proper 4xx/5xx responses.
* [ ] Jobs/events added only if needed.
* [ ] Tests: unit + integration + e2e green.

---

##### B) New external service (example: **YooKassa**)

**1. Domain**

* `app/domain/entities/payment.py` — state & transitions (`mark_paid`, `mark_failed`, `require_capture`).
* `app/domain/ports/payments.py` — provider contract:

```python
class PaymentProviderPort(Protocol):
    async def create_payment(...)->ProviderCreateResult: ...
    async def capture_payment(external_id: str, amount: Money): ...
    async def cancel_payment(external_id: str): ...
    async def refund_payment(external_id: str, ...): ...
    async def get_payment(external_id: str)->ProviderPayment: ...
    async def parse_webhook(headers: dict[str, str], body: bytes)->ProviderEvent: ...
```

* `app/domain/services/payments_service.py` — start/capture/cancel/webhook via provider port + UoW; after commit → event or job.

**2. Adapter (YooKassa)**

* `app/adapters/payments/yookassa/client.py` — httpx calls, webhook signature validation, retries.
* `app/adapters/payments/yookassa/schemas.py` — map API JSON ↔ internal provider types.
* `app/adapters/payments/yookassa/provider.py` — implements `PaymentProviderPort` (thin mapping).

**3. API & webhooks**

* `app/api/schemas/payments.py` — DTOs.
* `app/api/v1/payments.py` — start/capture/get.
* `app/api/v1/webhooks.py` — `POST /webhooks/yookassa` → `parse_webhook()` → `payments_service.handle_webhook()` → commit → event/job.

**4. DI**

* `app/core/di.py` binds `PaymentProviderPort` → `YooKassaProvider()` via `APP_PAYMENTS_PROVIDER=yookassa`.

**5. Workers**

* `app/workers/jobs/payments.py` — receipts, reconciliation, nightly capture.
* `app/workers/schedules.py` — reconciliation cron.
* `app/workers/consumers/payment_events.py` — react to `PaymentStatusChanged`.

**6. Tests**

* Unit: service with mocked provider.
* Integration: provider with YooKassa fixtures.
* E2E: start → webhook → status converges.

---

#### 4) Feature development flow (AI checklist)

1. **Domain first**: entities/ports/services — no IO.
2. **API**: DTOs & endpoints; use deps from `api/deps/*`.
3. **Adapters**: implement repo for chosen DB + migrations; bind in `core/di.py`.
4. **Background/Events**: simple → job after commit; complex/multi‑consumers → event + consumers.
5. **Observability**: metrics & tracing for critical paths.
6. **Security/Rate‑limit**: scopes, throttling for hot routes.
7. **Tests**: unit → integration → e2e.
8. **Docs/ADR**: update when architectural decisions change.

---

#### 5) Don’t forget (checklists)

**Universal**

* [ ] Types everywhere; avoid `Any` unless justified.
* [ ] IO only behind ports; no SQL/HTTP in domain/services.
* [ ] One `AsyncSession` per request/UoW; do not share across awaits.
* [ ] httpx: timeouts/limits; retries only where safe.
* [ ] Redis keys namespaced; TTL for caches.
* [ ] JWT secrets via env; never hardcode.
* [ ] Proper 4xx/5xx mapping and error bodies.
* [ ] Webhook idempotency (dedupe by provider event id).
* [ ] Side‑effects only after `commit()`.

**DB**

* [ ] PG migrations created & applied; indexes on hot paths.
* [ ] Mongo indexes created at client init.
* [ ] Use cursor‑pagination for large lists.

**Workers/Events**

* [ ] Consumers are idempotent (store processed ids).
* [ ] Retry policy + DLQ for poison messages.
* [ ] Version topics (`*.v1`) for schema evolution.

**Performance**

* [ ] Check N+1; prefetch/joins where needed.
* [ ] Cache hot reads; invalidate on write via jobs/events.

---

#### 6) Minimal templates (copy‑paste)

**Endpoint** — `app/api/v1/posts.py`

```python
router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("", response_model=PostRead, status_code=201)
async def create_post(payload: PostCreate, uow: Annotated[UnitOfWorkPort, Depends(get_uow)]):
    post = await post_service.create_post(payload, uow)
    return PostRead.model_validate(post)
```

**Service** — `app/domain/services/post_service.py`

```python
async def create_post(dto: PostCreateDTO, uow: UnitOfWorkPort) -> Post:
    post = Post.from_dto(dto)
    await uow.posts.create(post)
    await uow.commit()
    return post
```

**Repository (PG)** — `app/adapters/db/postgres/repositories/post_repo.py`

```python
class PgPostRepo(PostRepoPort):
    def __init__(self, session: AsyncSession):
        self.s = session
    async def get(self, post_id: UUID) -> Post | None: ...
    async def create(self, post: Post) -> Post: ...
    async def update(self, post: Post) -> None: ...
```

**Job** — `app/workers/jobs/posts.py`

```python
async def post_published(post_id: UUID):
    # idempotent side-effect
    ...
```

**Consumer** — `app/workers/consumers/post_events.py`

```python
@consumer(topic=TOPIC_POSTS)
async def on_post_published(msg: Message[PostPublished], jobs=posts_jobs):
    await jobs.post_published(UUID(msg.payload.post_id))
```

---

#### 7) PR & Review rules

* **Branch naming:** `feat/posts-publish` | `fix/payments-retry`.
* **PR template includes:** scope, files touched, migrations, tests, ops impact, feature flags, rollback plan.
* **Definition of Done:**

  * [ ] Matches file map & patterns.
  * [ ] Tests: unit + required integration + e2e.
  * [ ] Metrics/logs for critical path are updated.
  * [ ] Security & rate‑limits considered.
  * [ ] Docs/ADR updated if architecture changed.

---

##### TL;DR

1. Write the **domain first**, with no IO.
2. Endpoints are **thin**: DTO ↔ service.
3. All IO sits **behind ports** in **adapters**.
4. Side‑effects **only after commit**.
5. Prefer **jobs** by default; introduce **events** when reactions multiply or reliability is required.
6. Tests on three levels: unit → integration → e2e.

---

## Frontend Technology Stack & Development Flow ⚠️ **CRITICAL**

### **Current Frontend Stack**
- **Core Framework**: Next.js 15 (App Router) with React 19
- **Language**: TypeScript (strict mode enabled)
- **Styling System**: Tailwind CSS + Radix UI (shadcn/ui components)
- **State Management**: Redux Toolkit (RTK) with async thunks
- **Icons**: react-icons library (fa6 → bi → hi priority system)
- **Internationalization**: next-intl for 5-language support
- **Architecture**: Feature-Sliced Design (FSD) with strict import rules
- **HTTP Client**: Custom API client with auth + error handling
- **Package Management**: npm with package-lock.json
- **Build System**: Next.js built-in webpack + SWC compiler
- **Development**: Hot reload with file watching via polling
- **Quality Tools**: ESLint + TypeScript compiler + Prettier

### **Frontend Development Flow** ⚠️ **CRITICAL**

**Every time you write/modify frontend code, follow this systematic flow:**

#### 1. **Text Content** → **Localization (i18n)**
- ✅ **Check existing keys** in ALL 5 language files (`en.json`, `es.json`, `ru.json`, `ar.json`, `zh.json`)
- ✅ **Plan i18n key structure** for new text content (`feature.component.element[.state]`)
- ✅ **Add translation keys to ALL 5 language files** before writing component code
- ✅ **Use `useTranslations()` hook** or `t()` function in components
- ❌ **NEVER hardcode text strings** in components

#### 2. **Interactive Elements** (Links, Buttons, Sections) → **Icon + Cursor Pattern**
- ✅ **Add icon first**: All buttons/links MUST start with icon, then localized text
- ✅ **Centralized Icon Import**: ALL icons MUST be imported from `@/shared/ui/icons` - NEVER directly from react-icons
- ✅ **React-Icons Priority System** (for icons.tsx only):
  1. **First Priority**: `import { Fa* } from 'react-icons/fa6'` (Font Awesome 6 - preferred)
  2. **Second Priority**: `import { Bi* } from 'react-icons/bi'` (Bootstrap Icons - if fa6 doesn't have it)
  3. **Third Priority**: `import { Hi* } from 'react-icons/hi'` (Heroicons - last resort)
  4. **Never use**: inline SVG or other icon libraries
- ✅ **Use IconButton**: `responsive={true}` for adaptive behavior (icon-only below 1280px)
- ✅ **Cursor pointer**: All pressable elements MUST have `cursor-pointer` styling
- ✅ **Interactive states**: Provide clear hover, focus, and active states

#### 3. **Time/Date Values** → **Standardized Format**
- ✅ **Use format**: `%dd.%mm.%YYYY` (e.g., "01.01.2024") everywhere
- ✅ **Consistency**: Frontend display, backend responses, Telegram bot - same format
- ❌ **No other date formats** allowed

#### 4. **Component Creation** → **Theme + Border + Radius System**
- ✅ **Theme-aware**: Support both light & dark themes via CSS variables/tokens
- ✅ **No borders**: Use shadows for big/outer elements, backgrounds for small/inner elements
- ✅ **Border-radius consistency**:
  - Small/inner elements: `rounded-[0.75rem]` (buttons, inputs, avatars, icons)
  - Big/outer elements: `rounded-[1rem]` (boxes, containers, cards, sections)
- ✅ **Box containers**: Wrap ALL content in `Box` component from `@/shared/ui/box`
- ✅ **PageHeader**: Use for ALL pages/sections with proper icon color system

#### 5. **Architecture & Patterns** → **FSD + Redux + API Integration**
- ✅ **Follow FSD layers**: Higher layers → Lower layers only (app → widgets → features → entities → shared)
- ✅ **Redux Toolkit patterns**: Use `createSlice` and `createAsyncThunk` for state management
- ✅ **API integration**: Import types from `@/generated/api/schemas` for all API calls
- ✅ **Schema generation**: Run `npm run generate-schemas` after backend API changes
- ✅ **Component exports**: Always use public APIs via `index.ts` files
- ❌ **Cross-layer imports**: Never import between same-level layers
- ❌ **Manual API types**: Never create manual types - use generated schemas only

#### 6. **Validation Checklist Before Commit**
- ✅ All text uses i18n keys (no hardcoded strings)
- ✅ Interactive elements have icons + cursor-pointer + hover states
- ✅ ALL icons imported from `@/shared/ui/icons` - no direct react-icons imports
- ✅ Icons follow priority: fa6 → bi → hi (no inline SVG and Emoji)
- ✅ Dates use standardized format (%dd.%mm.%YYYY)
- ✅ Components work in light & dark themes
- ✅ Consistent border-radius (.75rem vs 1rem)
- ✅ No border classes used (shadows/backgrounds only)
- ✅ FSD architecture with correct import layers
- ✅ TypeScript strict mode compliance
- ✅ Use generated TypeScript schemas from `@/generated/api/schemas`
- ✅ No hardcoded API types - import from generated schemas
- ✅ Responsive design with Tailwind CSS
- ✅ Redux Toolkit for state management
- ✅ Error handling with toast notifications
- ✅ Run `npm run build` to validate FSD structure
- ✅ Run `npm run lint` for code quality

### **Key Frontend Architectural Patterns**

#### **Component Architecture Pattern**
```typescript
// ✅ Good: Feature-Sliced Design component structure
// File: features/posts/ui/PostCard.tsx
import { NewspaperIcon, CalendarIcon, EditIcon } from '@/shared/ui/icons';
import { useTranslations } from 'next-intl';
import { IconButton } from '@/shared/ui/icon-button';
import { Box } from '@/shared/ui/box';
import type { Post } from '@/entities/post';

interface PostCardProps {
  post: Post;
  onEdit?: (id: number) => void;
}

export const PostCard = ({ post, onEdit }: PostCardProps) => {
  const t = useTranslations('posts.card');

  return (
    <Box size="default" className="rounded-[1rem]">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400 w-10 h-10 rounded-[0.75rem] flex items-center justify-center">
            <NewspaperIcon size={20} />
          </div>
          <div>
            <h3 className="font-semibold">{post.title}</h3>
            <div className="flex items-center gap-1 text-sm text-muted-foreground">
              <CalendarIcon size={12} />
              {post.created_at}
            </div>
          </div>
        </div>
        {onEdit && (
          <IconButton
            variant="outline"
            icon={<EditIcon size={12} />}
            responsive
            onClick={() => onEdit(post.id)}
          >
            {t('actions.edit')}
          </IconButton>
        )}
      </div>
    </Box>
  );
};
```

#### **State Management Pattern**
```typescript
// ✅ Good: Redux Toolkit slice with async thunks
// File: entities/post/model/postSlice.ts
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import type { Post } from './types';
import { postsApi } from '../api';

interface PostsState {
  posts: Post[];
  loading: boolean;
  error: string | null;
  total: number;
}

export const fetchPosts = createAsyncThunk(
  'posts/fetchPosts',
  async (params: { category?: number; limit?: number; offset?: number }) => {
    const response = await postsApi.getPosts(params);
    return response;
  }
);

const postsSlice = createSlice({
  name: 'posts',
  initialState: {
    posts: [],
    loading: false,
    error: null,
    total: 0,
  } as PostsState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchPosts.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchPosts.fulfilled, (state, action) => {
        state.loading = false;
        state.posts = action.payload.posts;
        state.total = action.payload.count;
      })
      .addCase(fetchPosts.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch posts';
      });
  },
});

export const { clearError } = postsSlice.actions;
export default postsSlice.reducer;
```

#### **API Integration Pattern**
```typescript
// ✅ Good: Typed API client with auto-generated schemas
// File: entities/post/api/postsApi.ts
import { apiClient } from '@/shared/services/api';
// Import types from auto-generated OpenAPI schemas
import type {
  PostCreateRequest,
  PostResponse,
  PostsResponse,
  CategoriesGetRequest,
  CategoriesResponse
} from '@/generated/api/schemas';

export const postsApi = {
  async getPosts(params: CategoriesGetRequest): Promise<PostsResponse> {
    try {
      const response = await apiClient.post('/posts/get/', params);
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch posts');
    }
  },

  async createPost(data: PostCreateRequest): Promise<PostResponse> {
    try {
      const response = await apiClient.post('/posts/', data);
      return response.data;
    } catch (error) {
      throw new Error('Failed to create post');
    }
  },
};

// ✅ Good: Use generated schemas in components
// File: features/posts/ui/CreatePostForm.tsx
import type { PostCreateRequest } from '@/generated/api/schemas';

const handleSubmit = async (data: PostCreateRequest) => {
  await postsApi.createPost(data); // Fully typed with auto-completion
};
```

### **Quick Pattern Examples**
```typescript
// ✅ Good: Complete pattern implementation with centralized icons
import { PlusIcon, NewspaperIcon } from '@/shared/ui/icons';

<IconButton
  icon={<PlusIcon size={16} />}
  variant="success"
  responsive={true}
  className="cursor-pointer"
>
  {t('posts.actions.add')}
</IconButton>

// ✅ Good: Date formatting
const formattedDate = date.toLocaleDateString('en-GB'); // "01.01.2024"

// ✅ Good: Component structure with centralized icons
import { NewspaperIcon } from '@/shared/ui/icons';

<Box size="lg" className="rounded-[1rem]"> {/* Big/outer */}
  <PageHeader
    icon={<NewspaperIcon size={24} />}
    iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400 rounded-[0.75rem]" {/* Small/inner */}
    title={t('posts.header.title')}
    description={t('posts.header.description')}
  />
</Box>
```

---

## Components & UI System ⚠️ **CRITICAL**

> **Documentation Rule**: ALL component information MUST be documented in this section. Never create separate scattered blocks for component usage throughout CLAUDE.md. This consolidated section serves as the single source of truth for all component documentation.

### **Core UI Components**

#### **Box** - Universal Container
- **Import**: `import { Box } from '@/shared/ui/box'`
- **Purpose**: Single standard for ALL content containers, blocks, sections, and wrappers
- **Usage Rule**: EVERY content block MUST be wrapped in Box - no bare divs for containers
- **Sizes**: `sm` (p-3), `default` (p-4), `lg` (p-6)
- **Variants**: `default` (white/card), `muted` (subtle secondary), `accent` (highlighted)
- **Styling**: `rounded-[1rem]`, shadow system, theme-aware backgrounds

#### **Button & IconButton** - Interactive Elements
- **Import**: `import { Button } from '@/shared/ui/button'`, `import { IconButton } from '@/shared/ui/icon-button'`
- **IconButton Rule**: ALL buttons/links MUST start with icon, then localized text
- **Responsive Pattern**: Use `responsive={true}` for adaptive behavior (icon-only <1280px, icon+text ≥1280px)
- **Required**: `cursor-pointer` styling, clear hover/focus/active states
- **Icon Color**: Icon color MUST match text color - no separate icon coloring

#### **ButtonGroup** - Logical Grouping
- **Import**: `import { ButtonGroup } from '@/shared/ui/button-group'`
- **Purpose**: Group related buttons with shared borders and visual connection
- **Use Cases**: Edit+Delete, Save+Cancel, Upvote+Downvote, action clusters
- **Colors**: Use semantic colors (red=delete, green=add, etc.)

### **Layout Components**

#### **PageHeader** - Universal Page Headers ⚠️ **CRITICAL**
- **Import**: `import { PageHeader } from '@/shared/ui/page-header'`
- **Universal Usage**: EVERY page, demo component, admin section, content area MUST use PageHeader
- **Placement Rule**: PageHeader MUST be in page body, NEVER inside Box components
- **Structure**: `<div>` → `<PageHeader />` → `<Box>content</Box>`
- **Never Nest**: ❌ `<Box><PageHeader /></Box>` - PageHeader should be outside and above Box

**PageHeader Props**:
- **Icon**: Square colored container, `size={24}`, no border, `rounded-[0.75rem]`
- **Icon Colors**: Section-based system:
  - Posts: `bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400`
  - Space: `bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400`
  - Hub: `bg-orange-500/15 text-orange-600 dark:bg-orange-500/20 dark:text-orange-400`
  - Catalog: `bg-blue-500/15 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400`
  - Admin: `bg-red-500/15 text-red-600 dark:bg-red-500/20 dark:text-red-400`
  - Demo Components: Calculator=indigo, User=purple, Popup=orange, Toast=green
- **Title**: SEO-optimized page title
- **Description**: Additional context/breadcrumbs
- **Actions**: Button groups on right side

#### **ThreeColumnLayout** - Flexible Grid System
- **Import**: `import { ThreeColumnLayout } from '@/widgets/three-column-layout'`
- **Adaptive**: Auto-adjusts based on provided sidebars
- **Sticky**: Sidebars use `sticky top-20` (80px offset for header)
- **Usage**: `leftSidebar={<>multiple widgets</>}` `rightSidebar={<>widgets</>}`

#### **SidebarCard** - Unified Sidebar Interface
- **Import**: `import { SidebarCard } from '@/shared/ui/sidebar-card'`
- **Rule**: ALL sidebar widgets MUST use SidebarCard for consistent styling
- **Header**: Optional `title` + `icon` props (icon size 20px)
- **Content Spacing**: `sm` (space-y-4), `default` (space-y-6), `lg` (space-y-8)
- **Never**: Manual `<div className="flex items-center gap-2">` headers

### **Widget Components**

#### **Available Sidebar Widgets**
- **SectionsSidebar**: `import { SectionsSidebar } from '@/widgets/sections-sidebar'` - Business navigation sections
- **FiltersSidebar**: `import { FiltersSidebar } from '@/widgets/filters-sidebar'` - Time/sort filters
- **FastActionsSidebar**: `import { FastActionsSidebar } from '@/widgets/fast-actions-sidebar'` - Quick action buttons
- **ContactFormSidebar**: `import { ContactFormSidebar } from '@/widgets/contact-form-sidebar'` - Contact form widget
- **QuestionnaireSidebar**: `import { QuestionnaireSidebar } from '@/widgets/questionnaire-sidebar'` - Interactive surveys
- **AdminSidebar**: `import { AdminSidebar } from '@/widgets/admin-sidebar'` - Admin navigation

### **Icon System** ⚠️ **CRITICAL**

#### **Centralized Icon Management**
- **Rule**: ALL icons MUST be imported from `@/shared/ui/icons` - NEVER directly from react-icons
- **React-Icons Priority** (for icons.tsx file only): 1. `fa6` (Font Awesome 6), 2. `bi` (Bootstrap Icons), 3. `hi` (Heroicons)
- **Never Use**: Inline SVG, other icon libraries, direct react-icons imports in components

#### **Icon Usage Patterns**
- **Interactive Elements**: Icon color matches text color, no separate coloring
- **Standalone Icons**: Square containers `rounded-[0.75rem]`, icon full opacity, background low opacity
- **Default Styling**: `bg-muted text-muted-foreground` for neutral icons
- **Themed Pattern**: `bg-{color}-500/15 text-{color}-600 dark:bg-{color}-500/20 dark:text-{color}-400`

### **Styling System**

#### **Interactive Elements (Frontend Development Flow Step 2):**
- Icon + Text Structure: All buttons/links start with icon, then localized text
- Use `IconButton` with `responsive={true}` for adaptive behavior
- `cursor-pointer` styling for all pressable elements
- Clear hover, focus, and active states

#### **Component Styling (Frontend Development Flow Step 4):**
- Theme-aware: light & dark mode support via CSS variables
- No borders: shadows for big/outer, backgrounds for small/inner
- Border-radius: `.75rem` (small/inner) vs `1rem` (big/outer)
- Interactive shadows: Big/outer components use Card-style shadow with hover effects:
  - Shadow: `shadow-[0_0.25rem_1.5rem_rgba(0,0,0,0.12)]`
  - Transition: `transition-all duration-300 ease-[cubic-bezier(0,0,0.5,1)]`
  - Hover effect: `hover:scale-[1.01]` (subtle scale animation)

#### **Icon & Color Styling:**
- **Interactive Elements (Buttons/Links)**: Icon color MUST match text color - no separate icon coloring. Use `IconButton` with `responsive={true}` for adaptive text hiding (below 1280px shows icons only, 1280px+ shows icons + text).
- **Standalone Icon Containers**: Independent icons (avatars, PageHeader, category icons) MUST use rounded square containers (`rounded-[0.75rem]`). Icon at full opacity, background at low opacity.
- **Default Icon Styling**: `bg-muted text-muted-foreground` for neutral/default standalone icons.
- **Colored Icon Pattern**: `bg-{color}-500/15 text-{color}-600 dark:bg-{color}-500/20 dark:text-{color}-400` for themed icons.
- **Opacity Standards**: Background opacity 15% (light) / 20% (dark), icon/text at full opacity for proper contrast.

#### **Border-Radius Standards:**
- **Small/Inside Elements**: Use `rounded-[0.75rem]` (0.75rem) for inner and small elements: buttons, inputs, dropdown items, avatars, standalone icon containers, ...
- **Large/Outside Elements**: Use `rounded-[1rem]` (1rem) for outer and big elements: boxes, page containers, major sections, content boxes, containers

#### **Theme System**
- **Theme-Aware**: All components support light & dark themes via CSS variables
- **No Borders**: Use shadows for big/outer elements, backgrounds for small/inner elements
- **Interactive Shadows**: `shadow-[0_0.25rem_1.5rem_rgba(0,0,0,0.12)]` with `hover:scale-[1.01]` animation

### **Usage Examples**

```typescript
// ✅ Complete Component Pattern
import { PlusIcon, NewspaperIcon, EditIcon, TrashIcon } from '@/shared/ui/icons';

// Page structure with proper hierarchy
<div className="max-w-2xl mx-auto">
  <PageHeader
    icon={<NewspaperIcon size={24} />}
    iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400"
    title={t('posts.title')}
    description={t('posts.description')}
    actions={
      <ButtonGroup>
        <IconButton icon={<PlusIcon size={16} />} variant="success" responsive>
          {t('add')}
        </IconButton>
      </ButtonGroup>
    }
  />

  <Box size="lg">
    <div className="space-y-6">
      {/* Content inside Box */}

      <ButtonGroup>
        <IconButton variant="outline" icon={<EditIcon size={12} />} responsive>
          Edit
        </IconButton>
        <IconButton variant="destructive" icon={<TrashIcon size={12} />} responsive>
          Delete
        </IconButton>
      </ButtonGroup>

      {/* Nested box for secondary content */}
      <Box variant="muted" size="default">
        <h3>Usage Examples</h3>
        <p>Secondary content...</p>
      </Box>
    </div>
  </Box>
</div>

// ✅ Three-column layout with sidebars
<ThreeColumnLayout
  leftSidebar={
    <>
      <SectionsSidebar />
      <FiltersSidebar />
    </>
  }
  rightSidebar={
    <>
      <FastActionsSidebar />
      <ContactFormSidebar />
    </>
  }
>
  <div className="space-y-8">
    {/* Main content */}
  </div>
</ThreeColumnLayout>

// ✅ Sidebar with proper SidebarCard usage
<SidebarCard
  title={t('filters')}
  icon={<FilterIcon size={20} />}
  contentSpacing="default"
>
  <div className="space-y-6">
    {/* Sidebar content */}
  </div>
</SidebarCard>
```

### **Component Creation Rules**
1. **Layer Placement**: Basic UI → `shared/ui/`, Complex compositions → `widgets/`, Feature-specific → `features/*/ui/`
2. **Naming**: PascalCase components, kebab-case folders, match file names
3. **Public APIs**: Export through `index.ts`, never direct imports
4. **FSD Rules**: Higher layers → Lower layers only, no cross-layer imports
5. **❌ NEVER CREATE DEMO COMPONENTS IN `shared/ui/`**: Demo components (like `CounterDemo`, `UserDemo`, `MultiImageUploadDemo`) belong in `features/demo/components/`, NOT in `shared/ui/`. The `shared/ui/` layer is exclusively for reusable base components (Button, Input, ImageUpload, etc.) that have no business logic or state.

---

## Development Commands

### Local Development
```bash
# Start full local development environment
make up

# Start only databases (Redis, MongoDB)
make up-base

# Frontend development (from frontend/ directory)
npm run dev        # Start Next.js dev server
npm run build      # Build for production
npm run lint       # Run ESLint
```

### Docker Environments
```bash
make up-dev        # Development environment
make up-prod       # Production environment
make up-test       # Test environment
make down          # Stop services
make status        # Check container status
```

### Testing
```bash
make test          # Run all tests (API + Web)
make test-backend  # Backend tests only
make test-web      # Frontend tests only
make unit-test     # Run pytest unit tests
```

### Code Quality
```bash
make lint          # Lint Python code with pylint
make clean         # Clean Python cache files
```

### Debugging & Monitoring
```bash
make shell         # Connect to API container
make db-shell      # Connect to MongoDB
make logs-api      # View API logs
make logs-jobs     # View background jobs logs
make logs-tg       # View Telegram bot logs
```

### API Development & Schema Generation

#### **Schema-First Development Workflow**
1. **Backend**: Write FastAPI endpoints with proper Pydantic models (descriptions, examples)
2. **Generate**: Run `cd frontend && npm run generate-schemas` after API changes
3. **Frontend**: Import types from `@/generated/api/schemas` in all API-related code
4. **Validate**: Check http://localhost/docs for API documentation accuracy

```bash
# Generate TypeScript schemas from OpenAPI (after backend changes)
cd frontend && npm run generate-schemas

# Check what containers are running
docker ps

# View API logs in real-time
docker logs -f web-api-1

# API Documentation (when containers are running)
# OpenAPI/Swagger UI: http://localhost/docs
# OpenAPI JSON: http://localhost/openapi.json
```

**Important**: Never create manual API types. Always use generated schemas for type safety and consistency.

## Architecture

### Backend (FastAPI + Python)
- **Location**: `backend/app/`
- **Main entry**: `backend/app/main.py`
- **Routes**: Organized in `routes/` by feature (users, posts, categories, payments, reviews)
- **Models**: MongoDB models in `models/` using `consys` library
- **Services**: Middleware and utilities in `services/`
- **Dependencies**: Uses `uv` for package management, defined in `pyproject.toml`

#### **API Schema Generation Rules**
- **Clean Pydantic Models**: All request/response models MUST use proper Pydantic field descriptions and examples
- **OpenAPI Tags**: Organize endpoints with proper tags for clean schema generation
- **Response Models**: Always specify `response_model` in FastAPI decorators for accurate schemas
- **Documentation**: Use docstrings and Pydantic field descriptions for auto-generated API docs
- **Schema Location**: Generated TypeScript schemas available in `frontend/src/generated/api/`

#### **API Documentation**
- **Live Documentation**: http://localhost/docs (Swagger UI)
- **OpenAPI Spec**: http://localhost/openapi.json
- **Generated Types**: `frontend/src/generated/api/schemas.ts`
- **Usage**: Import types from generated schemas in frontend code

### Frontend Architecture (Feature-Sliced Design)

#### **FSD Layer Structure**
```
frontend/src/
├── app/                      # Next.js App Router (routes, page compositions)
├── widgets/                  # Complex UI compositions
├── features/                 # User-facing functionality
├── entities/                 # Business domain logic
├── shared/                   # Reusable infrastructure
├── providers/                # App-wide providers
├── generated/                # Auto-generated code (OpenAPI schemas)
└── i18n/                    # Internationalization config
```

#### **FSD Import Rules** ⚠️ **CRITICAL**
1. **Higher layers can import from lower layers only**:
   - `app/` → `widgets/`, `features/`, `entities/`, `shared/`
   - `widgets/` → `features/`, `entities/`, `shared/`
   - `features/` → `entities/`, `shared/`
   - `entities/` → `shared/` only
   - `shared/` → no internal dependencies

2. **Cross-layer imports** (same level) are forbidden:
   - ❌ `features/posts/` → `features/auth/`
   - ❌ `widgets/header/` → `widgets/sidebar/`
   - ✅ Use `entities/` or `shared/` for communication

3. **Public API only**: Import through `index.ts` files, not direct paths:
   - ✅ `import { PostCard } from '@/widgets/posts-list'`
   - ❌ `import { PostCard } from '@/widgets/posts-list/ui/PostCard'`

#### **Layer Responsibilities**

**`widgets/`** - Complex UI blocks
- `header/` - Navigation and user menu
- `posts-list/` - Posts grid with filtering
- `feedback-system/` - Toasts, popups, notifications
- `user-profile/` - User profile components

**`features/`** - User-facing functionality
- `navigation/` - Language switching, routing
- `demo/` - Demo components and state
- `user/` - User settings and initialization

**`entities/`** - Business domain models
- `user/` - User types, API calls, utilities
- `post/` - Post types, API calls, utilities
- `category/` - Category types, API calls, utilities

**`shared/`** - Infrastructure layer
- `ui/` - **Pure UI components ONLY** (Button, Input, ImageUpload, etc.) - **❌ NO demo components, NO business logic, NO state**
- `lib/` - Utilities and helpers
- `services/api/` - HTTP client and auth
- `stores/` - Global Redux state
- `hooks/` - Reusable React hooks
- `constants/` - App constants
- `config/` - Configuration

#### **File Organization**
Each FSD slice follows this structure:
```
feature-name/
├── ui/           # React components
├── model/        # State, types, business logic
├── lib/          # Utilities specific to this slice
├── api/          # API calls (entities only)
└── index.ts      # Public API exports
```

---

## Backend Technology Stack & Coding Flow ⚠️ **CRITICAL**

### **Current Backend Stack**
- **Core Framework**: FastAPI (async Python web framework)
- **Language**: Python 3.11+ with type hints and async/await
- **Database**: MongoDB with custom ConSys library for ODM
- **Package Management**: uv (fast Python package installer)
- **Logging**: loguru for structured JSON logging
- **Authentication**: JWT tokens with FastAPI security
- **Background Tasks**: Celery with Redis broker
- **API Documentation**: OpenAPI/Swagger auto-generated
- **Testing**: pytest with async test support
- **Validation**: Pydantic v2 for request/response models
- **HTTP Client**: httpx for async external API calls
- **Monitoring**: Prometheus metrics collection
- **Caching**: Redis for session storage and caching

### **Backend Development Flow** ⚠️ **CRITICAL**

**Every time you write/modify backend code, follow this systematic flow:**

#### 1. **Models & Schema** → **Pydantic + ConSys**
- ✅ **Define Pydantic models** for request/response validation
- ✅ **Use ConSys models** for MongoDB document structure
- ✅ **Type annotations** required for all functions and variables
- ✅ **Field validation** with Pydantic validators when needed
- ❌ **NEVER skip type hints** or input validation

#### 2. **API Endpoints** → **Async FastAPI Pattern**
- ✅ **Async route handlers** for all endpoints (`async def`)
- ✅ **Dependency injection** for database, auth, logging
- ✅ **HTTP method mapping** (POST for data queries, GET for simple retrieval)
- ✅ **Response models** defined with Pydantic
- ✅ **Error handling** with FastAPI HTTPException
- ❌ **NEVER use sync operations** in async contexts

#### 3. **Database Operations** → **ConSys ODM**
- ✅ **ConSys models** for MongoDB document structure
- ✅ **Async database operations** using ConSys async methods
- ✅ **Query optimization** with proper indexing
- ✅ **Transaction support** for critical operations
- ❌ **NEVER direct MongoDB queries** without ConSys

#### 4. **Logging & Monitoring** → **Structured Logging**
- ✅ **loguru logger** for all logging operations
- ✅ **JSON structured logs** for production parsing
- ✅ **Request/response logging** with correlation IDs
- ✅ **Error tracking** with stack traces
- ❌ **NEVER log sensitive data** (passwords, tokens, PII)

#### 5. **Schema Generation** → **Clean OpenAPI Generation**
- ✅ **Pydantic field descriptions** for all model fields to generate clear API docs
- ✅ **Response models** specified in all FastAPI decorators (`response_model=`)
- ✅ **OpenAPI tags** for logical endpoint grouping
- ✅ **Field examples** in Pydantic models for better generated documentation
- ✅ **Generate schemas** after API changes: `cd frontend && npm run generate-schemas`

#### 6. **Testing & Quality**
- ✅ **pytest async tests** for all endpoints
- ✅ **Test fixtures** for database setup/teardown
- ✅ **Mock external dependencies** with httpx_mock
- ✅ **Run `make unit-test`** before commit
- ✅ **Coverage reporting** with minimum 80% threshold

**Backend Code Pattern Examples:**
```python
# ✅ Good: Complete FastAPI endpoint with all patterns
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from loguru import logger
from typing import List, Optional
import httpx

# Pydantic models for validation & schema generation
class PostCreateRequest(BaseModel):
    """Request model for creating a new post"""
    title: str = Field(..., min_length=1, max_length=200,
                      description="Post title", example="My Awesome Post")
    content: str = Field(..., min_length=1,
                        description="Post content in markdown",
                        example="This is the post content...")
    category_id: int = Field(..., gt=0,
                            description="Category ID", example=1)

class PostResponse(BaseModel):
    """Response model for post data"""
    id: int = Field(description="Post ID", example=1)
    title: str = Field(description="Post title", example="My Awesome Post")
    content: str = Field(description="Post content", example="Content...")
    created_at: str = Field(description="Creation date (DD.MM.YYYY)",
                           example="01.01.2024")
    category: Optional[str] = Field(None, description="Category name",
                                   example="Technology")

# ConSys model for MongoDB
class PostDocument(ConsysModel):
    title: str
    content: str
    category_id: int
    created_at: datetime
    status: int = 1

# Async endpoint with proper error handling & schema generation
@router.post("/posts/", response_model=PostResponse, tags=["Posts"])
async def create_post(
    request: PostCreateRequest,
    db: Database = Depends(get_database),
    current_user: User = Depends(get_current_user)
) -> PostResponse:
    try:
        logger.info(f"Creating post for user {current_user.id}",
                   extra={"user_id": current_user.id, "action": "create_post"})

        # ConSys database operation
        post_doc = PostDocument(
            title=request.title,
            content=request.content,
            category_id=request.category_id,
            created_at=datetime.utcnow()
        )

        result = await db.posts.insert_one(post_doc.dict())

        logger.info(f"Post created successfully",
                   extra={"post_id": result.inserted_id})

        return PostResponse(
            id=result.inserted_id,
            title=post_doc.title,
            content=post_doc.content,
            created_at=post_doc.created_at.strftime('%d.%m.%Y')
        )

    except Exception as e:
        logger.error(f"Failed to create post: {str(e)}",
                    extra={"error": str(e), "user_id": current_user.id})
        raise HTTPException(status_code=500, detail="Failed to create post")

# ✅ Good: Async external API call
async def fetch_external_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"External API request failed: {e}")
            raise HTTPException(status_code=503, detail="External service unavailable")
```

**Backend Validation Checklist:**
1. ✅ All endpoints use async/await patterns
2. ✅ Pydantic models with field descriptions and examples for schema generation
3. ✅ Response models specified in FastAPI decorators (`response_model=`)
4. ✅ OpenAPI tags for endpoint organization
5. ✅ ConSys models for MongoDB operations
6. ✅ Structured logging with loguru
7. ✅ Type hints on all functions and variables
8. ✅ Error handling with proper HTTP status codes
9. ✅ Tests cover all critical paths
10. ✅ No sensitive data in logs
11. ✅ Generate TypeScript schemas after API changes (`npm run generate-schemas`)


### Key Technologies
- **Frontend**: Next.js 15, React 19, TypeScript, Redux Toolkit, Tailwind CSS, Radix UI
- **Backend**: FastAPI, MongoDB (via consys), Redis, Socket.IO, Prometheus monitoring
- **Infrastructure**: Docker, NGINX, Let's Encrypt, Grafana

### Docker & Deployment Architecture

#### **Multi-Stage Dockerfile Strategy**
- **Frontend Dockerfile**: Uses multi-stage build with `development` and `runner` (production) stages
- **Development Stage**: Includes dev dependencies, hot reload support, file watching with polling
- **Production Stage**: Optimized build with production dependencies only, pre-built app
- **Best Practice**: Single Dockerfile with multiple stages ensures consistency across environments

#### **Docker Compose File Structure**
The project uses a base + override pattern for different environments:

**Base Configuration:**
- `docker-compose.yml` - Common service definitions, defaults to production (`runner` stage)

**Environment Overrides:**
- `docker-compose.local.yml` - Local development (databases + nginx + hot reload)
  - Uses `development` stage for frontend
  - Adds Redis, MongoDB, NGINX server
  - Enables volume mounting for hot reload
  - Usage: `make up` (base + local)

- `docker-compose.dev.yml` - Remote development environment
  - Same as local but for remote dev servers
  - Uses `development` stage for frontend
  - Usage: `make up-dev` (base + dev)

- `docker-compose.prod.yml` - Production deployment
  - Uses `runner` stage for optimized builds
  - Adds production services (jobs, telegram bot)
  - Production environment variables
  - Usage: `make up-prod` (base + prod)

- `docker-compose.base.yml` - Infrastructure only
  - Just databases and monitoring (Redis, MongoDB, Prometheus, Grafana)
  - Usage: `make up-base` (infrastructure only)

#### **Makefile Integration**
```bash
make up          # Local: base + local.yml (full dev environment)
make up-dev      # Remote dev: base + dev.yml
make up-prod     # Production: base + prod.yml
make up-base     # Infrastructure: base.yml only
```

#### **Hot Reload Configuration**
- **Local Development**: Volume mounting + Next.js file watching with polling
- **Frontend**: `development` stage with `npm run dev`
- **Backend**: Volume mounting + uvicorn `--reload` flag
- **File Watching**: Next.js configured with webpack polling for Docker compatibility

### Frontend Guidelines

#### **Path Aliases**
```typescript
@/              → src/
@/entities/*    → src/entities/*
@/features/*    → src/features/*
@/widgets/*     → src/widgets/*
@/shared/*      → src/shared/*
```

#### **Internationalization (i18n) - Implementation Details**
> **Main Rule**: Follow **Frontend Development Flow Step 1** for all text content

**Technical Implementation:**
- Use `next-intl` with typed helpers: `t('namespace.key')`
- Keep messages under `frontend/messages/<locale>/*.json`
- Server components: pass translated content via props
- Client components: use `useTranslations` hook
- Key naming: `feature.component.element[.state]`

**Supported Languages:** The project supports 5 languages with message files in `frontend/messages/`:
- `en.json` (English - primary/source language)
- `ar.json` (Arabic)
- `es.json` (Spanish)
- `ru.json` (Russian)
- `zh.json` (Chinese)

**Complete Localization Process:**
1. **NEVER hardcode text strings** - All user-visible text MUST go through i18n system
2. **Check ALL language files** - Before writing frontend code, check what keys already exist across all 5 language files
3. **Add missing keys to ALL languages** - When adding new text, you MUST add the localization key to all 5 language files simultaneously
4. **Maintain key consistency** - Use the same key structure across all language files
5. **Meaningful translations** - Provide appropriate translations for each language, not just English text copied

**Key Naming Convention:**
```
feature.component.element[.state]
```
Examples:
- `posts.card.title` - Post card title
- `auth.login.button.submit` - Login submit button
- `navigation.menu.items.posts` - Posts menu item
- `demo.counter.button.increment` - Counter increment button
- `errors.validation.required` - Required field validation error

**Localization Code Flow:**
1. **Plan the text content** - Identify all user-visible strings needed
2. **Check existing keys** - Search across all 5 language files for existing similar keys
3. **Add new keys** - Add to ALL 5 language files with appropriate translations:
   ```json
   // en.json
   {
     "posts": {
       "card": {
         "readMore": "Read More"
       }
     }
   }

   // es.json
   {
     "posts": {
       "card": {
         "readMore": "Leer Más"
       }
     }
   }

   // ru.json
   {
     "posts": {
       "card": {
         "readMore": "Читать далее"
       }
     }
   }

   // ar.json
   {
     "posts": {
       "card": {
         "readMore": "اقرأ المزيد"
       }
     }
   }

   // zh.json
   {
     "posts": {
       "card": {
         "readMore": "阅读更多"
       }
     }
   }
   ```
4. **Use keys in components** - Reference the i18n keys in React components:
   ```typescript
   import { useTranslations } from 'next-intl';

   const PostCard = () => {
     const t = useTranslations('posts.card');

     return (
       <IconButton icon={<ReadIcon size={16} />} responsive>
         {t('readMore')}
       </IconButton>
     );
   };
   ```

**Translation Quality Standards:**
- **Contextual accuracy** - Translations should fit the UI context and component purpose
- **Consistent terminology** - Use the same terms across the app for identical concepts
- **Cultural appropriateness** - Consider cultural context for each target language
- **Length considerations** - Account for text expansion/contraction in different languages
- **RTL support** - Arabic text requires right-to-left layout considerations

**Quick Reference - Follow Frontend Development Flow:**
> **See "Frontend Development Flow" section above for complete workflow**

**Localization Checklist (from Frontend Development Flow Step 1):**
1. ✅ Check existing keys in ALL 5 language files
2. ✅ Plan i18n key structure for new text content
3. ✅ Add translation keys to ALL 5 language files before coding
4. ✅ Use `useTranslations()` hook or `t()` function in components
5. ✅ Test text renders correctly in different languages
6. ❌ Never commit components with hardcoded text strings

**Common Localization Patterns:**
```typescript
import { PlusIcon, NewspaperIcon } from '@/shared/ui/icons';

// Page headers with localized title/description
<PageHeader
  icon={<NewspaperIcon size={24} />}
  title={t('posts.header.title')}
  description={t('posts.header.description')}
  // ... other props
/>

// Button text localization
<IconButton icon={<PlusIcon size={16} />} variant="success" responsive>
  {t('posts.actions.add')}
</IconButton>

// Form validation messages
{errors.title && <span className="text-red-500">{t('validation.required')}</span>}

// Toast/notification messages
toast.success(t('posts.actions.deleteSuccess'));
toast.error(t('posts.actions.deleteError'));
```

#### Theming (Light + Dark)
- Implement styles with *CSS variables/Tailwind tokens* only; *no hex values* inline.
- Provide theme-aware colors via design tokens; respect system preference when applicable.
- Components must look correct in both themes. Add examples/stories for each.

#### Feedback (Toasts/Popups)
- Use `widgets/feedback-system` components for all user feedback.
- Map severities to variants: `success`, `error`, `warning`, `info`.
- Never use `window.alert()` for UX feedback.
- Import: `import { ToastProvider, useToast } from '@/widgets/feedback-system'`

#### Components / UI
- **Pure UI**: Use `@/shared/ui` for basic components (buttons, inputs, boxes)
- **Complex UI**: Create widgets for compositions (header, lists, forms)
- **Feature UI**: Components specific to one feature go in `features/*/ui/`
- Prefer *Server Components* by default; mark clients with `"use client"`.
- Use *shadcn/ui* patterns: `cn()` for class merge, `cva` for variants.
- Accessibility: label form controls, provide `aria-label` for icon buttons.


#### State Management (Redux Toolkit)
- **Global state**: `shared/stores/` (auth, theme, app-wide data)
- **Feature state**: Each feature manages its own state in `stores/`
- **Entity state**: Business logic state in `entities/*/model/`
- Keep slices focused; prefer RTK patterns with `createAsyncThunk`.
- Avoid duplicating server data; normalize when needed.

#### API Integration
- **API client**: Use `shared/services/api/client.ts` for HTTP requests
- **Entity APIs**: Business domain APIs in `entities/*/api/`
- **Feature APIs**: Feature-specific APIs in `features/*/api/`
- **Base URL**:
  - Frontend (local): `http://localhost/` (via nginx proxy)
  - Backend (local): `http://localhost/api/` (via nginx proxy)
- **Response Format**: Backend returns `{"categories": [...]}`, `{"posts": [...], "count": N}`
- **Response Types**: Import all types from `@/generated/api/schemas` - never create manual types
- **Schema Generation**: Run `npm run generate-schemas` after backend API changes
- Handle auth, retries, timeouts, and typed errors centrally
- Surface errors via `widgets/feedback-system`, never raw stack traces
- **Mock Fallback**: Set `NEXT_PUBLIC_USE_MOCK_FALLBACK=true` to enable mock data during development

#### **Component Creation Guidelines**
1. **Determine the right layer**:
   - Basic UI → `shared/ui/`
   - Complex composition → `widgets/`
   - Feature-specific → `features/*/ui/`
   - Business entity → `entities/*/ui/`

2. **Follow naming conventions**:
   - Components: PascalCase (`UserProfile`, `PostCard`)
   - Files: match component name (`UserProfile.tsx`)
   - Folders: kebab-case (`user-profile/`, `posts-list/`)

3. **Export through index.ts**:
   ```typescript
   // widgets/posts-list/index.ts
   export { PostCard } from './ui/PostCard';
   export { PostsGrid } from './ui/PostsGrid';
   ```

### Backend Guidelines (FastAPI)
- Use *async* endpoints; prefer `httpx.AsyncClient` for external calls.
- Pydantic models for request/response; validate input strictly.
- Log with structure (json) and never log secrets/PII.
- Add integration tests for critical endpoints; unit tests for services.
- Use dependency overrides/mocks in tests; isolate DB state per test module when needed.

### Testing & Quality Gates
- Before committing, Claude should run:
1. `npm run build` to ensure FSD import rules are followed
2. `npm run lint` for code quality
3. `make test-web` when touching frontend logic
4. `make unit-test` for backend changes
- Add/adjust tests for every behavior change.
- Snapshot/UI tests: keep snapshots small and meaningful.

### Git & PR Workflow
- *Conventional Commits*: `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, `test:`…
- Small PRs (<300 LOC); include a concise summary and checklist (tests, i18n, a11y, dark mode).
- If Claude introduces breaking changes, use `feat!: …` and document migration.

### Security & Privacy
- *Do not* read or modify `.env*`, `secrets/**`, `infra/**/prod/*`, CI tokens, or deployment keys.
- No outbound network calls without approval.
- Redact secrets in logs; avoid printing tokens or personal data.
- Sanitize user input; encode/escape HTML; never interpolate untrusted strings into HTML.

### Claude Code Permissions (policy)
- *Allowed* (common): `Read`, `Edit`, `Write`; `Bash(git status:*)`, `Bash(git diff:*)`; `npm run lint|build|test`; `make test*`.
- *Ask*: `git push`, installing packages, DB migrations, Docker builds/pushes, hitting external APIs.
- *Deny*: `rm -rf`, `curl` to arbitrary hosts, touching secrets, prod config, or CI variables.

### Files & Paths Not To Touch
- `.env*`, `secrets/**`, `infra/**/prod/**`, `infra/nginx/**`, `infra/compose/**` (production variants), CI config unless explicitly asked.

### Deployment & API Access
- Environment configuration via `.env` file (see `base.env` template)
- Docker Compose configurations for different environments in `infra/compose/`
- NGINX reverse proxy configuration in `infra/nginx/`
- **API Access**:
  - **Via Nginx Proxy**: `http://localhost/api/` (recommended for frontend integration)
  - **Direct Access**: `http://api:5000/` (exposed port for direct backend testing)
- **Port Mapping**:
  - Frontend: `http://localhost/` (nginx:80 → web:3000)
  - API (proxied): `http://localhost/api/` (nginx:80 → api:5000)
  - API (direct): `http://api:5000/` (host:5000 → api:5000)
- **Direct API Testing**: Use curl commands with either proxy URL or direct port 5000

### How to Work in This Repo (Claude checklist)
1. **Follow Frontend Development Flow**: Use the 5-step systematic flow for ALL frontend code
2. **Respect FSD architecture**: check import rules and layer responsibilities before coding
3. **Explain the plan** (brief) and show a *unified diff* preview before writing
4. **Make minimal changes** in relevant files only
5. **Run validation**: `npm run build` (FSD structure) + `npm run lint` (code quality)
6. **Run tests**: `make test-web` (frontend) + `make unit-test` (backend) when applicable
7. **Propose commit**: Conventional Commits format + short PR description

### **Quick Reference - Where to Put Code**

| Type | Location | Example |
|------|----------|---------|
| Basic UI (Button, Input, Box) | `shared/ui/` | `shared/ui/button.tsx` |
| Enhanced UI (IconButton, Box, PageHeader) | `shared/ui/` | `shared/ui/icon-button.tsx` |
| **❌ Demo Components (CounterDemo, UserDemo)** | **❌ NEVER `shared/ui/`** → **✅ `features/demo/components/`** | **✅ `features/demo/components/CounterDemo.tsx`** |
| Layout Systems (Three-Column) | `widgets/three-column-layout/` | `widgets/three-column-layout/ui/ThreeColumnLayout.tsx` |
| Sidebar Widgets (Sections, Filters, Actions) | `widgets/*-sidebar/` | `widgets/sections-sidebar/ui/SectionsSidebar.tsx` |
| Header, Navigation | `widgets/header/` | `widgets/header/ui/Header.tsx` |
| User auth logic | `features/auth/` | `features/auth/ui/LoginForm.tsx` |
| User data types | `entities/user/` | `entities/user/model/user.ts` |
| HTTP client | `shared/services/` | `shared/services/api/client.ts` |
| App config | `shared/config/` | `shared/config/app.ts` |
| Page composition | `app/` | `app/[locale]/page.tsx` |
| Auto-generated | `generated/` | `generated/api/schemas.ts` |

**Component Documentation**: All component usage, patterns, and examples are documented in the **Components & UI System** section above. Refer to that section for detailed component information.

⚠️ **Remember**: Higher layers → Lower layers only. No cross-layer imports. Use public APIs via `index.ts`.

## Documentation Guidelines

**IMPORTANT: Do not create new files for documentation or examples** including:
- ❌ No new .md files to describe logic, usage, or implementation details
- ❌ No example .json files to show data structures or logging formats
- ❌ No separate documentation files of any format

Instead:
- ✅ Write documentation directly in code files as comments and docstrings
- ✅ Add relevant information to this CLAUDE.md file
- ✅ Update the main README.md if necessary
- ✅ Use inline code documentation for complex logic
- ✅ Include data structure examples directly in docstrings

This keeps documentation consolidated and prevents proliferation of scattered files throughout the codebase. All documentation should be embedded within the actual code that uses it.

**CLAUDE.md Component Documentation Rule** ⚠️ **CRITICAL**:
- ✅ ALL component information MUST be documented in the **Components & UI System** section only
- ✅ Component usage patterns, examples, and best practices belong in that consolidated section
- ❌ NEVER create separate scattered blocks for component documentation throughout CLAUDE.md
- ❌ NEVER duplicate component information in multiple sections
- 🔄 When adding new components: update the **Components & UI System** section with usage patterns and examples
