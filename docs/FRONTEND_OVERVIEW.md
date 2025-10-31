# Frontend Overview

## Structure

```
app/
  layout.tsx               # Root app layout
  [locale]/layout.tsx      # Locale-aware shell with providers
  [locale]/page.tsx        # SEO landing page
  [locale]/posts/page.tsx  # Public posts listing
  [locale]/dashboard/page.tsx
  [locale]/(auth)/login    # Auth routes
  api/health/route.ts      # Platform health endpoint
components/
  ui/                      # shadcn-inspired primitives
  layout/                  # Header/Footer
  posts/, dashboard/       # Domain-specific client components
config/
  i18n.ts, api.ts          # Locale + API constants
features/
  auth/, posts/            # Feature folders with hooks/components
hooks/                      # Reusable hooks (auth, redux)
lib/                        # API client, utilities, schemas
providers/                  # App-level providers (theme, redux, query, locale)
store/                      # Redux Toolkit slices
styles/globals.css          # Tailwind entrypoint
```

## Key Concepts

- **App Router**: Locale is a dynamic segment (`/[locale]`). Server components render layout/shell; client components manage interactive features.
- **Localization**: `next-intl` powers translations. Messages live in `public/locales/<locale>/common.json`. Add namespaces per domain as needed.
- **Theming**: `next-themes` toggles system/default themes via `data-theme` attribute. Tailwind tokens defined in CSS custom properties.
- **State & Data**: Redux Toolkit holds auth session state; React Query handles remote caching and background revalidation.
- **API Layer**: `lib/api-client.ts` centralizes Axios configuration and attaches bearer tokens. Feature-specific hooks emit typed data using `zod` schemas.
- **UI Primitives**: `components/ui` contains composable, accessible building blocks (Button, Card, Input, etc.). Extend via `shadcn/ui` CLI if desired.
- **Testing**: Vitest + Testing Library for unit tests (`pnpm test`). Configure additional suites (e2e, visual regression) under `frontend/tests` or `frontend/e2e`.

## Running Locally

```
make install-frontend
make dev-frontend
```

Next.js runs at `http://localhost:3000`. Configure API base URL via `NEXT_PUBLIC_API_URL`.

## Extending Features

1. Add API hooks in `features/<domain>/api` using React Query and zod parsing.
2. Create components/pages under `app/[locale]` using UI primitives.
3. Update locale messages in `public/locales/...`.
4. Add tests in `frontend/tests`.
5. Wire Redux slices if global state is required; prefer co-locating state within feature folders.
