# AI Development Workflow Playbook

This checklist is designed for copilots such as Codex CLI and Claude Code. Follow it sequentially whenever generating new functionality.

1. **Understand context**
   - Inspect relevant files with `rg`, `tree`, or directory listings.
   - Review domain models (`backend/app/models/`), schemas, and route patterns before generating code.
   - Capture environment constraints (locales, themes, time zones, RBAC policies) from `docs/` and config modules.

2. **Plan explicitly**
   - Summarise the change, inputs, outputs, and affected layers (models, services, routes, frontend views, tests).
   - Break the plan into steps and confirm with the human if scope is ambiguous.

3. **Data model + migrations**
   - Modify SQLAlchemy models and generate Alembic migrations.
   - Keep migrations idempotent and append-only.
   - Update `frontend/lib/schemas/*.ts` or regenerate via `scripts/export_schemas.py` (to be built per domain).

4. **Backend implementation**
   - Extend Pydantic schemas, services, and API routes.
   - Register background tasks if work requires async processing (`@periodic_task`, `@event_handler`, `@sequential_task`).
   - Log meaningful events with Loguru and surface errors to Sentry.

5. **Backend tests**
   - Write unit/integration tests under `backend/tests/` targeting models, services, and routes.
   - Maintain ≥ 90% coverage; aim for 100% on new modules.
   - Use Faker and fixtures in `conftest.py` for deterministic data.

6. **Documentation**
   - Update or create docs in `docs/` outlining new flows, dependencies, or operational runbooks.
   - Note feature flags, environment variables, and migration steps.

7. **Generate OpenAPI + TS schemas**
   - Run `uv run scripts/export_openapi.py` (to be implemented) to refresh contracts.
   - Convert relevant models to zod or TypeScript interfaces (`frontend/lib/schemas`).

8. **Frontend implementation**
   - Add API hooks under `frontend/features/*/api` and components/pages in `frontend/app`.
   - Ensure components respect responsive breakpoints, themes (`data-theme`), and locales via `next-intl`.
   - Reuse UI primitives in `frontend/components/ui` to maintain visual consistency.

9. **Frontend tests**
   - Cover critical UI logic with Vitest + Testing Library (`frontend/tests`).
   - Consider adding Playwright scenarios for complex flows.

10. **Verification**
   - Run `make test-backend`, `make test-frontend`, `make lint-backend`, and `make lint-frontend`.
   - Update docs or scripts if manual steps were required.

11. **Deployment readiness**
   - For release work, update Docker images, Compose/Swarm manifests, and GitHub Actions as needed.
   - Document rollout instructions, feature flags, and backout plans in `docs/RELEASE_NOTES.md` (create when required).

### Prompting Tips

- Reference files explicitly (e.g., “Update `backend/app/services/payments.py` to add Stripe client method…”).
- Ask the AI to produce diff-friendly output; avoid rewriting large files unless necessary.
- Re-run search commands after code generation to validate replacements.
- Always request tests unless explicitly out of scope.
- Defer to existing conventions; if uncertain, ask for clarification instead of guessing.

This workflow keeps AI contributions predictable, reviewable, and production ready.
