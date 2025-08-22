# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Full-stack web application with Python FastAPI backend, Next.js frontend, and Telegram bot. The application uses Docker containers for deployment and includes monitoring via Prometheus/Grafana.

---

## Golden Rules for Claude
- **Minimal, focused diffs**: change only what’s necessary; keep PRs small (<300 LOC) and self-contained.
- **Never hard-code secrets** or credentials; never read or write `.env`, `secrets/`, or CI secrets.
- **Always respect i18n**: all user-visible strings must go through the localization system (see *Frontend Guidelines*).
- **Theme-aware UI**: every component must work in **light & dark** themes via tokens/CSS variables (no hardcoded colors).
- **Use toasts/popups for feedback**: errors/warnings/success/info should use app toasts/dialogs, not `alert()` or raw text.
- **Accessibility first**: proper aria labels/roles, focus states, keyboard nav; no color-only affordances.
- **Ask before destructive or external actions** (network, DB migrations, Docker, `git push`, etc.).

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

## Architecture

### Backend (FastAPI + Python)
- **Location**: `backend/app/`
- **Main entry**: `backend/app/main.py`
- **Routes**: Organized in `routes/` by feature (users, posts, categories, payments, reviews)
- **Models**: MongoDB models in `models/` using `consys` library
- **Services**: Middleware and utilities in `services/`
- **Dependencies**: Uses `uv` for package management, defined in `pyproject.toml`

### Frontend (Next.js + TypeScript)
- **Location**: `frontend/src/`
- **App Router**: Using Next.js 15 App Router in `app/[locale]/`
- **Internationalization**: `next-intl` for multi-language support
- **State Management**: Redux Toolkit with slices in `lib/redux/`
- **API Client**: Centralized API client in `lib/api/client.ts` with auth handling
- **Styling**: Using Shadcn/UI: Tailwind CSS + Radix UI components
- **Path Alias**: `@/` maps to `src/`

### Key Technologies
- **Frontend**: Next.js 15, React 19, TypeScript, Redux Toolkit, Tailwind CSS, Radix UI
- **Backend**: FastAPI, MongoDB (via consys), Redis, Socket.IO, Prometheus monitoring
- **Infrastructure**: Docker, NGINX, Let's Encrypt, Grafana

### Frontend Guidelines
#### Internationalization (i18n)
- *All user-facing strings* must use `next-intl` (no hardcoded text).
Use typed helpers: `t('namespace.key')`.
- Keep messages under `frontend/src/messages/<locale>/*.json`.
- For server components, pass translated content via props; for client components, use the `useTranslations` hook.
- Keys: `feature.scope.action` (e.g., `auth.login.error.invalidCredentials`).

#### Theming (Light + Dark)
- Implement styles with *CSS variables/Tailwind tokens* only; *no hex values* inline.
- Provide theme-aware colors via design tokens; respect system preference when applicable.
- Components must look correct in both themes. Add examples/stories for each.

#### Feedback (Toasts/Popups)
- Use the shared *Toaster Provider* (Radix Toast / shadcn toast) mounted at app root.
- Map severities to variants: `success`, `error`, `warning`, `info`.
Never use `window.alert()` for UX feedback.

#### Components / UI
- Prefer *Server Components* by default; mark clients with `"use client"`.
- Use *shadcn/ui* patterns: `cn()` for class merge, `cva` for variants, avoid ad-hoc Tailwind overrides.
- Accessibility: label form controls, provide `aria-label` for icon buttons, maintain focus order and visible focus.

#### State (Redux Toolkit)
- Keep slices focused; colocate selectors; prefer RTK patterns (immutability via Immer, action creators, `createAsyncThunk` for async).
- Avoid duplicating server data; normalize when needed.

#### API Client
- Centralize fetch in `lib/api/client.ts`; handle auth (token), retries, timeouts, and typed errors.
- UI surfaces errors via toasts/dialogs; never leak raw stack traces to users.

### Backend Guidelines (FastAPI)
- Use *async* endpoints; prefer `httpx.AsyncClient` for external calls.
- Pydantic models for request/response; validate input strictly.
- Log with structure (json) and never log secrets/PII.
- Add integration tests for critical endpoints; unit tests for services.
- Use dependency overrides/mocks in tests; isolate DB state per test module when needed.

### Testing & Quality Gates
- Before committing, Claude should run:
1. `make unit-test` (or narrower scope if touching backend only)
2. `make test-web` when touching frontend logic
3. `npm run lint` and Python `make lint`
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

### Deployment
- Environment configuration via `.env` file (see `base.env` template)
- Docker Compose configurations for different environments in `infra/compose/`
- NGINX reverse proxy configuration in `infra/nginx/`

### How to Work in This Repo (Claude checklist)
1. Explain the plan (brief) and show a *unified diff* preview before writing.
2. Make *minimal* changes in relevant files only.
3. Ensure i18n keys exist; make UI theme-aware; use toasts/popups for feedback.
4. Run tests/linters; include fixes if failing.
5. Propose commit message (Conventional Commits) and a short PR description.
