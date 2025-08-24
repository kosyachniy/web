# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Full-stack web application with Python FastAPI backend, Next.js frontend, and Telegram bot. The application uses Docker containers for deployment and includes monitoring via Prometheus/Grafana.

---

## Golden Rules for Claude
- **Minimal, focused diffs**: change only what's necessary; keep PRs small (<300 LOC) and self-contained.
- **Never hard-code secrets** or credentials; never read or write `.env`, `secrets/`, or CI secrets.
- **Follow FSD Architecture**: respect Feature-Sliced Design layers and import rules (see *Frontend Architecture*).
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

### Frontend Architecture (Feature-Sliced Design)

#### **FSD Layer Structure**
```
frontend/src/
├── app/                      # Next.js App Router (routes, global configs)
├── page-layouts/             # Page compositions (combine widgets + features)
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
   - `page-layouts/` → `widgets/`, `features/`, `entities/`, `shared/`
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

**`page-layouts/`** - Page compositions
- Combine widgets + features for complete pages
- Page-specific logic and data fetching
- SEO and metadata management

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
- `ui/` - Pure UI components (shadcn/ui)
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

### Key Technologies
- **Frontend**: Next.js 15, React 19, TypeScript, Redux Toolkit, Tailwind CSS, Radix UI
- **Backend**: FastAPI, MongoDB (via consys), Redis, Socket.IO, Prometheus monitoring
- **Infrastructure**: Docker, NGINX, Let's Encrypt, Grafana

### Frontend Guidelines

#### **Path Aliases**
```typescript
@/              → src/
@/entities/*    → src/entities/*
@/features/*    → src/features/*
@/widgets/*     → src/widgets/*
@/shared/*      → src/shared/*
@/page-layouts/* → src/page-layouts/*
```

#### Internationalization (i18n)
- *All user-facing strings* must use `next-intl` (no hardcoded text).
Use typed helpers: `t('namespace.key')`.
- Keep messages under `frontend/messages/<locale>/*.json`.
- For server components, pass translated content via props; for client components, use the `useTranslations` hook.
- Keys: `feature.scope.action` (e.g., `auth.login.error.invalidCredentials`).

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
- **Pure UI**: Use `@/shared/ui` for basic components (buttons, inputs, cards)
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
- Handle auth, retries, timeouts, and typed errors centrally
- Surface errors via `widgets/feedback-system`, never raw stack traces

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

### Deployment
- Environment configuration via `.env` file (see `base.env` template)
- Docker Compose configurations for different environments in `infra/compose/`
- NGINX reverse proxy configuration in `infra/nginx/`

### How to Work in This Repo (Claude checklist)
1. **Respect FSD architecture**: check import rules and layer responsibilities before coding.
2. Explain the plan (brief) and show a *unified diff* preview before writing.
3. Make *minimal* changes in relevant files only.
4. Ensure i18n keys exist; make UI theme-aware; use feedback widgets.
5. Run `npm run build` to validate FSD structure; fix any import violations.
6. Run tests/linters; include fixes if failing.
7. Propose commit message (Conventional Commits) and a short PR description.

### **Quick Reference - Where to Put Code**

| Type | Location | Example |
|------|----------|---------|
| Button, Input, Card | `shared/ui/` | `shared/ui/button.tsx` |
| Header, Navigation | `widgets/header/` | `widgets/header/ui/Header.tsx` |
| User auth logic | `features/auth/` | `features/auth/ui/LoginForm.tsx` |
| User data types | `entities/user/` | `entities/user/model/user.ts` |
| HTTP client | `shared/services/` | `shared/services/api/client.ts` |
| App config | `shared/config/` | `shared/config/app.ts` |
| Page composition | `page-layouts/` | `page-layouts/home/ui/HomePage.tsx` |
| Auto-generated | `generated/` | `generated/api/schemas.ts` |

⚠️ **Remember**: Higher layers → Lower layers only. No cross-layer imports. Use public APIs via `index.ts`.
