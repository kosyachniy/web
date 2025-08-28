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
- **Consistent border-radius**: use `rounded-[0.75rem]` for small/inside elements (buttons, inputs, dropdown items, avatars) and `rounded-[1rem]` for big/outside elements (cards, dialogs, containers). Never use `rounded-sm`, `rounded-md`, or `rounded-lg`.
- **No borders, use backgrounds/shadows**: never use `border` classes. Small components (buttons, inputs, tags) use colored or gray backgrounds. Big components (cards, dialogs, containers) use shadows with white/background colors since they contain small components with colored backgrounds.
- **Use toasts/popups for feedback**: errors/warnings/success/info should use app toasts/dialogs, not `alert()` or raw text.
- **Centralized icon system**: use only icons from `@/shared/ui/icons` - never import from `react-icons` directly or use inline SVG. All icons must be solid/filled style (no outlined icons).
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

### Frontend Guidelines

#### **Path Aliases**
```typescript
@/              → src/
@/entities/*    → src/entities/*
@/features/*    → src/features/*
@/widgets/*     → src/widgets/*
@/shared/*      → src/shared/*
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

#### **Frontend Structure & Design Rules** ⚠️ **CRITICAL**

**Button & Link Pattern:**
- **Icon + Text Structure**: All buttons and links MUST start with an icon, followed by localized text (e.g., `+ Add Category`)
- **Responsive Design**: Use `IconButton` with `responsive={true}` for adaptive behavior - show only icon on small screens, icon + text on larger screens
- **Components**: Use `IconButton` from `@/shared/ui/icon-button` instead of plain `Button` for new implementations

**Cursor & Interaction:**
- **Pointer Cursor**: All pressable elements (buttons, links, clickable cards) MUST have `cursor-pointer` styling
- **Interactive States**: Provide clear hover, focus, and active states for all interactive elements

**Box & Container Styling:**
- **Box Containers**: Every content block MUST be wrapped in a `Box` component from `@/shared/ui/box`
- **Box vs Card**: Use `Box` for main content containers; `Card` only for specific card-like content (post cards, admin lists)
- **Size Variants**:
  - `size="sm"` - Small containers with minimal padding (`p-3`)
  - `size="default"` - Standard containers with normal padding (`p-4`)
  - `size="lg"` - Large containers for main content areas (`p-6`)
- **Background Variants**:
  - `variant="default"` - Standard white/card background with shadow
  - `variant="muted"` - Subtle muted background for secondary content
  - `variant="accent"` - Accent background for highlighted content
- **Consistent Styling**: All boxes have consistent border-radius, shadow, and theme-aware backgrounds

**Page Structure:**
- **Page Headers**: Every page and component section MUST start with `PageHeader` component:
  - **Universal Usage**: ALL pages, demo components, admin sections, and content areas must use PageHeader
  - **Icon**: Square colored icon container (width = height) with rounded background, no border
  - **Color System**: Section-based colors with background/text variants:
    - **Posts**: `bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400`
    - **Space**: `bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400`
    - **Hub**: `bg-orange-500/15 text-orange-600 dark:bg-orange-500/20 dark:text-orange-400`
    - **Catalog**: `bg-blue-500/15 text-blue-600 dark:bg-blue-500/20 dark:text-blue-400`
    - **Categories**: `bg-indigo-500/15 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400`
    - **Admin**: `bg-red-500/15 text-red-600 dark:bg-red-500/20 dark:text-red-400`
    - **Demo Components**: Use specific colors per component type (Calculator=indigo, User=purple, Popup=orange, Toast=green)
  - **Title**: SEO-optimized page title positioned to the right of icon
  - **Description**: Additional context or breadcrumbs under the title
  - **Actions**: Action buttons or button groups on the right side of the header
  - **No Custom Headers**: Never create custom `<header>` or `<h1>` elements when PageHeader should be used
- **Import**: `import { PageHeader } from '@/shared/ui/page-header'`

**Button Grouping:**
- **Logical Groups**: Group related buttons using `ButtonGroup` component from `@/shared/ui/button-group`
- **Shared Borders**: Grouped buttons share common border-radius and are visually connected
- **Semantic Colors**: Use appropriate colors for actions (red for delete, green for add, etc.)
- **Examples**: Edit + Delete, Upvote + Downvote, Save + Cancel

**Border-Radius Standards:**
- **Small/Inside Elements**: Use `rounded-[0.75rem]` (0.75rem) for buttons, inputs, small boxes
- **Large/Outside Elements**: Use `rounded-[1rem]` (1rem) for cards, page containers, major sections
- **Consistency**: Never use other radius values without explicit design system approval

**Three-Column Layout System:**
- **ThreeColumnLayout**: Use `@/widgets/three-column-layout` for flexible 3-column layouts
- **Adaptive Columns**: Layout automatically adjusts based on which sidebars are provided
- **Sidebar Widgets**: Reusable sidebar components in `@/widgets/*-sidebar/` for consistent functionality
- **Sticky Positioning**: Sidebars use `sticky top-20` (80px) to account for header height (`h-16` = 64px + spacing)
- **Examples**:
  ```typescript
  // Full 3-column layout
  <ThreeColumnLayout
    leftSidebar={<><SectionsSidebar /><FiltersSidebar /></>}
    rightSidebar={<><FastActionsSidebar /><ContactFormSidebar /></>}
  >
    <YourContent />
  </ThreeColumnLayout>

  // Left sidebar only
  <ThreeColumnLayout leftSidebar={<SectionsSidebar />}>
    <YourContent />
  </ThreeColumnLayout>
  ```

**Available Sidebar Widgets:**
- **Left Sidebar**: `SectionsSidebar` (navigation), `FiltersSidebar` (time/sort filters)
- **Right Sidebar**: `FastActionsSidebar` (quick actions), `ContactFormSidebar`, `QuestionnaireSidebar`
- **Admin Sidebar**: `AdminSidebar` (admin navigation) in `AdminLayout`
- **All Sidebars**: Use `Box` containers with `sticky top-20` positioning to avoid header overlap

**Sidebar & Layout Elements:**
- **Box Wrapping**: Wrap sidebar elements (categories, filters, author info, etc.) in `Box` containers
- **Logical Grouping**: Each functional group gets its own box (e.g., separate boxes for categories, filters, actions)
- **Hierarchy**: Use box size variants to establish visual hierarchy (larger boxes for primary content)

**When to Use PageHeader:**
- **Always Required**: Every page (`/posts`, `/space`, `/hub`, `/catalog`, admin pages)
- **Demo Components**: Replace `CardHeader` with `PageHeader` in demo components
- **Content Sections**: Any section that has title + description should use PageHeader
- **Never Use**: Custom `<header>`, standalone `<h1>`, `CardHeader` for main sections

**Component Examples:**
```typescript
// Good: Icon + Text button with responsive behavior
<IconButton
  icon={<AddIcon size={16} />}
  variant="success"
  responsive
>
  Add Category
</IconButton>

// Good: Button group with semantic colors
<ButtonGroup>
  <IconButton variant="outline" icon={<EditIcon size={12} />} responsive>Edit</IconButton>
  <IconButton variant="destructive" icon={<DeleteIcon size={12} />} responsive>Delete</IconButton>
</ButtonGroup>

// Good: Page header with proper color system (pages)
<PageHeader
  icon={<PostsIcon size={24} />}
  iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400"
  title={t('posts')}
  description="Browse and discover posts organized by categories"
  actions={<IconButton icon={<AddIcon size={16} />} variant="success" responsive>Add Post</IconButton>}
/>

// Good: Demo component headers with specific icons/colors
<PageHeader
  icon={<CalculatorIcon size={24} />}
  iconClassName="bg-indigo-500/15 text-indigo-600 dark:bg-indigo-500/20 dark:text-indigo-400"
  title={t('counter.title')}
  description={t('counter.description')}
/>

<PageHeader
  icon={<UserIcon size={24} />}
  iconClassName="bg-purple-500/15 text-purple-600 dark:bg-purple-500/20 dark:text-purple-400"
  title={t('userSettings.title')}
  description={t('userSettings.description')}
/>

// Good: Content wrapped in Box with nested structure
<Box size="lg">
  <PageHeader {...headerProps} />
  <div className="space-y-6">
    <div>Main content...</div>

    {/* Nested box for code examples or secondary content */}
    <Box variant="muted" size="default">
      <h3 className="font-semibold mb-2">Usage Examples:</h3>
      <div className="text-sm text-muted-foreground space-y-2">
        <p><code>example()</code> - Description</p>
      </div>
    </Box>
  </div>
</Box>

// Good: Three-column layout with multiple sidebar blocks
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
      <QuestionnaireSidebar />
    </>
  }
>
  <div className="space-y-8">
    <YourMainContent />
  </div>
</ThreeColumnLayout>
```

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
| Basic UI (Button, Input, Card) | `shared/ui/` | `shared/ui/button.tsx` |
| Enhanced UI (IconButton, Box, PageHeader) | `shared/ui/` | `shared/ui/icon-button.tsx` |
| Layout Systems (Three-Column) | `widgets/three-column-layout/` | `widgets/three-column-layout/ui/ThreeColumnLayout.tsx` |
| Sidebar Widgets (Sections, Filters, Actions) | `widgets/*-sidebar/` | `widgets/sections-sidebar/ui/SectionsSidebar.tsx` |
| Header, Navigation | `widgets/header/` | `widgets/header/ui/Header.tsx` |
| User auth logic | `features/auth/` | `features/auth/ui/LoginForm.tsx` |
| User data types | `entities/user/` | `entities/user/model/user.ts` |
| HTTP client | `shared/services/` | `shared/services/api/client.ts` |
| App config | `shared/config/` | `shared/config/app.ts` |
| Page composition | `app/` | `app/[locale]/page.tsx` |
| Auto-generated | `generated/` | `generated/api/schemas.ts` |

**New Component Quick Reference:**
- **IconButton**: `import { IconButton } from '@/shared/ui/icon-button'` - Icon + text buttons with responsive behavior
- **ButtonGroup**: `import { ButtonGroup } from '@/shared/ui/button-group'` - Logical grouping of related buttons
- **Box**: `import { Box } from '@/shared/ui/box'` - Container with consistent styling (border, background, shadow)
- **PageHeader**: `import { PageHeader } from '@/shared/ui/page-header'` - Standard page header with square icon, title, description, actions
- **ThreeColumnLayout**: `import { ThreeColumnLayout } from '@/widgets/three-column-layout'` - Flexible 3-column layout with adaptive sidebars
- **Sidebar Widgets**:
  - `import { SectionsSidebar } from '@/widgets/sections-sidebar'` - Business navigation sections
  - `import { FiltersSidebar } from '@/widgets/filters-sidebar'` - Time/sort filters
  - `import { FastActionsSidebar } from '@/widgets/fast-actions-sidebar'` - Quick action buttons
  - `import { ContactFormSidebar } from '@/widgets/contact-form-sidebar'` - Contact form widget
  - `import { QuestionnaireSidebar } from '@/widgets/questionnaire-sidebar'` - Interactive feedback survey
- **Demo Component Icons**:
  - Counter Demo: `CalculatorIcon` with indigo colors (`bg-indigo-500/15 text-indigo-600`)
  - User Demo: `UserIcon` with purple colors (`bg-purple-500/15 text-purple-600`)
  - Popup Demo: `WindowIcon` with orange colors (`bg-orange-500/15 text-orange-600`)
  - Toast Demo: `BellIcon` with green colors (`bg-green-500/15 text-green-600`)
- **Icons**: `import { PostsIcon, AddIcon, EditIcon, CalculatorIcon, UserIcon, WindowIcon, BellIcon } from '@/shared/ui/icons'` - Solid style icons with size prop

⚠️ **Remember**: Higher layers → Lower layers only. No cross-layer imports. Use public APIs via `index.ts`.
