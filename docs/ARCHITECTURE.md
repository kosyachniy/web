# AI-Native Project Template Architecture

This repository provides an opinionated, but extensible, mono-repo baseline for teams shipping AI-assisted products. It combines a FastAPI backend, Next.js frontend, and infrastructure glue (Docker, GitHub Actions, NGINX) that are tuned for iterative development with copilots such as Codex CLI and Claude Code.

## High-Level Layout

```
backend/   # FastAPI service with async task engine, auth, RBAC, integrations
frontend/  # Next.js app router project with theming, i18n, Redux Toolkit
infra/     # Docker, NGINX, and Swarm deployment manifests
scripts/   # Utility scripts for local DX and CI hooks
docs/      # Architectural decisions, AI workflow playbooks, onboarding
```

## Core Principles

- **AI-ready** – Stable, predictable scaffolding so LLMs can inspect context and generate features with minimal friction.
- **Security & compliance** – Opinionated defaults for authentication, authorization, audit trails, error reporting, and secret management.
- **Scalability without ceremony** – Clean layering, dependency injection via FastAPI, minimal global state, and async-first networking.
- **Multi-tenant delivery** – Unified API consumed by web, mobile, and bots with typed contracts shared to the frontend (zod) and external consumers (OpenAPI).
- **Productivity** – Hot reload in dev, reproducible Docker builds, typed tooling, and test harnesses for rapid feedback.

## Backend Highlights

- FastAPI with `sqlalchemy 2.x` async ORM, PostgreSQL, and Redis.
- Loguru logging, Sentry tracing, and structured task instrumentation.
- Authentication flow supporting password, social/OAuth placeholders, and pre-auth session snapshots stored in Redis.
- Role-based access control (RBAC) service and policy helpers for route guards.
- Async task registry with periodic, sequential, and event-driven jobs runnable in-process or by a separate worker.
- Base HTTP client abstraction for integrating external providers (payments, messaging, etc.).
- Alembic migrations seeded with `users`, `posts`, and login audit trails.

## Frontend Highlights

- Next.js App Router, React 18, and TypeScript with strict mode.
- Shared providers for Redux Toolkit, React Query, theming, and localization.
- Radix UI primitives and shadcn-inspired UI kit to stay accessible and theme-ready.
- Mobile-first, universal components for landing, posts, dashboard, and auth flows.
- Localization scaffold for five locales with `next-intl`.
- Vitest + Testing Library harness for unit tests; extends easily to Playwright for e2e.

## Infrastructure Highlights

- Dockerfiles for backend and frontend with multi-stage builds.
- `docker-compose.yml` for local dev and integration testing (backend + frontend + Postgres + Redis).
- Production-oriented compose stack for Docker Swarm with NGINX reverse proxy and certbot hook points.
- GitHub Actions workflows for linting, testing, Docker image publishing, and Swarm deployment.

## AI Workflow Guardrails

The [AI_WORKFLOW](./AI_WORKFLOW.md) guide documents a repeatable flow for copilots: inspect repo → plan → sync models/migrations → generate backend code/tests → emit OpenAPI/TS schemas → build frontend → verify localization/theme/accessibility → run tests/linters. Prompts in that doc explicitly reference repo structure so AI models stay on track.

## Extending the Template

- Add new domains under `backend/app/models` + `schemas` + `api/v1/routes` with matching migrations.
- Mirror data contracts in `frontend/lib/schemas` (or generate via tooling).
- Register background jobs in `backend/app/tasks/jobs.py` using the `@periodic_task`, `@event_handler`, or `@sequential_task` decorators.
- Drop integration clients into `backend/app/clients` and corresponding service abstractions under `backend/app/services`.
- Wire additional CI stages in `.github/workflows/ci.yml` and extend Docker stacks under `infra/`.

Adopt this baseline as-is or fork and adapt the conventions to your team. Every module includes docstrings and minimal comments designed to help AI agents understand intent without getting lost in implementation noise.
