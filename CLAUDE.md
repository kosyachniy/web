# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

Full-stack web application with Python FastAPI backend, Next.js frontend, and Telegram bot. The application uses Docker containers for deployment and includes monitoring via Prometheus/Grafana.

---

## Golden Rules for Claude
- **Frontend Development**: Follow the **Frontend Development Flow (UltraThink)** below for ALL frontend code changes
- **Minimal, focused diffs**: change only what's necessary; keep PRs small (<300 LOC) and self-contained
- **Follow FSD Architecture**: respect Feature-Sliced Design layers and import rules (see *Frontend Architecture*)
- **Never hard-code secrets** or credentials; never read or write `.env`, `secrets/`, or CI secrets
- **Use toasts/popups for feedback**: errors/warnings/success/info should use app toasts/dialogs, not `alert()` or raw text
- **Centralized icon system**: use only icons from `@/shared/ui/icons` - never import from `react-icons` directly or use inline SVG
- **Special symbols vs icons**: use Unicode symbols (©, ®, ™) as text characters, not icons with backgrounds
- **Accessibility first**: proper aria labels/roles, focus states, keyboard nav; no color-only affordances
- **Ask before destructive or external actions** (network, DB migrations, Docker, `git push`, etc.)

---

## Frontend Development Flow (UltraThink) ⚠️ **CRITICAL**

**Every time you write/modify frontend code, follow this systematic flow:**

### 1. **Text Content** → **Localization (i18n)**
- ✅ **Check existing keys** in ALL 5 language files (`en.json`, `es.json`, `ru.json`, `ar.json`, `zh.json`)
- ✅ **Plan i18n key structure** for new text content (`feature.component.element[.state]`)
- ✅ **Add translation keys to ALL 5 language files** before writing component code
- ✅ **Use `useTranslations()` hook** or `t()` function in components
- ❌ **NEVER hardcode text strings** in components

### 2. **Interactive Elements** (Links, Buttons, Sections) → **Icon + Cursor Pattern**
- ✅ **Add icon first**: All buttons/links MUST start with icon, then localized text
- ✅ **Use IconButton**: `responsive={true}` for adaptive behavior (icon-only below 1280px)
- ✅ **Cursor pointer**: All pressable elements MUST have `cursor-pointer` styling
- ✅ **Interactive states**: Provide clear hover, focus, and active states

### 3. **Time/Date Values** → **Standardized Format**
- ✅ **Use format**: `%dd.%mm.%YYYY` (e.g., "01.01.2024") everywhere
- ✅ **Consistency**: Frontend display, backend responses, Telegram bot - same format
- ❌ **No other date formats** allowed

### 4. **Component Creation** → **Theme + Border + Radius System**
- ✅ **Theme-aware**: Support both light & dark themes via CSS variables/tokens
- ✅ **No borders**: Use shadows for big/outer elements, backgrounds for small/inner elements
- ✅ **Border-radius consistency**:
  - Small/inner elements: `rounded-[0.75rem]` (buttons, inputs, avatars, icons)
  - Big/outer elements: `rounded-[1rem]` (boxes, containers, cards, sections)
- ✅ **Box containers**: Wrap ALL content in `Box` component from `@/shared/ui/box`
- ✅ **PageHeader**: Use for ALL pages/sections with proper icon color system

### 5. **Validation Checklist Before Commit**
- ✅ All text uses i18n keys (no hardcoded strings)
- ✅ Interactive elements have icons + cursor-pointer + hover states
- ✅ Dates use standardized format (%dd.%mm.%YYYY)
- ✅ Components work in light & dark themes
- ✅ Consistent border-radius (.75rem vs 1rem)
- ✅ No border classes used (shadows/backgrounds only)
- ✅ Run `npm run build` to validate FSD structure
- ✅ Run `npm run lint` for code quality

**Quick Pattern Examples:**
```typescript
// ✅ Good: Complete pattern implementation
<IconButton
  icon={<AddIcon size={16} />}
  variant="success"
  responsive={true}
  className="cursor-pointer"
>
  {t('posts.actions.add')}
</IconButton>

// ✅ Good: Date formatting
const formattedDate = date.toLocaleDateString('en-GB'); // "01.01.2024"

// ✅ Good: Component structure
<Box size="lg" className="rounded-[1rem]"> {/* Big/outer */}
  <PageHeader
    icon={<PostsIcon size={24} />}
    iconClassName="bg-green-500/15 text-green-600 dark:bg-green-500/20 dark:text-green-400 rounded-[0.75rem]" {/* Small/inner */}
    title={t('posts.header.title')}
    description={t('posts.header.description')}
  />
</Box>
```

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

#### **Request/Response Patterns**
- **Categories Request**: `{"parent": 0, "status": 1, "locale": "en"}`
- **Categories Response**: `{"categories": [{"id": 1, "title": "News", "url": "news", "categories": [...]}]}`
- **Posts Request**: `{"category": 1, "limit": 12, "offset": 0, "search": "keyword"}`
- **Posts Response**: `{"posts": [...], "count": 42}`
- **Error Response**: `{"detail": "Error message"}` with appropriate HTTP status

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
> **Main Rule**: Follow **Frontend Development Flow (UltraThink) Step 1** for all text content

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

**Quick Reference - Follow UltraThink Flow:**
> **See "Frontend Development Flow (UltraThink)" section above for complete workflow**

**Localization Checklist (from UltraThink Step 1):**
1. ✅ Check existing keys in ALL 5 language files
2. ✅ Plan i18n key structure for new text content
3. ✅ Add translation keys to ALL 5 language files before coding
4. ✅ Use `useTranslations()` hook or `t()` function in components
5. ✅ Test text renders correctly in different languages
6. ❌ Never commit components with hardcoded text strings

**Common Localization Patterns:**
```typescript
// Page headers with localized title/description
<PageHeader
  title={t('posts.header.title')}
  description={t('posts.header.description')}
  // ... other props
/>

// Button text localization
<IconButton icon={<AddIcon size={16} />} variant="success" responsive>
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

#### **Frontend Structure & Design Rules** ⚠️ **CRITICAL**
> **Main Rule**: Follow **Frontend Development Flow (UltraThink) Steps 2-4** for all UI elements

**Interactive Elements (UltraThink Step 2):**
- Icon + Text Structure: All buttons/links start with icon, then localized text
- Use `IconButton` with `responsive={true}` for adaptive behavior
- `cursor-pointer` styling for all pressable elements
- Clear hover, focus, and active states

**Component Styling (UltraThink Step 4):**
- Theme-aware: light & dark mode support via CSS variables
- No borders: shadows for big/outer, backgrounds for small/inner
- Border-radius: `.75rem` (small/inner) vs `1rem` (big/outer)

**Box & Container Styling:**
- **Box Containers**: Every content block MUST be wrapped in a `Box` component from `@/shared/ui/box`
- **Universal Container**: Use `Box` for ALL content containers - it's the single standard for all content blocks, sections, and containers
- **Size Variants**:
  - `size="sm"` - Small containers with minimal padding (`p-3`)
  - `size="default"` - Standard containers with normal padding (`p-4`)
  - `size="lg"` - Large containers for main content areas (`p-6`)
- **Background Variants**:
  - `variant="default"` - Standard white/card background with shadow
  - `variant="muted"` - Subtle muted background for secondary content
  - `variant="accent"` - Accent background for highlighted content
- **Consistent Styling**: All boxes have consistent border-radius (`rounded-[1rem]`), unified shadow system (`0 0.25rem 1.5rem rgba(0,0,0,0.12)` with theme adaptation), and theme-aware backgrounds

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

**Icon & Color Styling:**
- **Interactive Elements (Buttons/Links)**: Icon color MUST match text color - no separate icon coloring. Use `IconButton` with `responsive={true}` for adaptive text hiding (below 1280px shows icons only, 1280px+ shows icons + text).
- **Standalone Icon Containers**: Independent icons (avatars, PageHeader, category icons) MUST use rounded square containers (`rounded-[0.75rem]`). Icon at full opacity, background at low opacity.
- **Default Icon Styling**: `bg-muted text-muted-foreground` for neutral/default standalone icons.
- **Colored Icon Pattern**: `bg-{color}-500/15 text-{color}-600 dark:bg-{color}-500/20 dark:text-{color}-400` for themed icons.
- **Opacity Standards**: Background opacity 15% (light) / 20% (dark), icon/text at full opacity for proper contrast.

**Border-Radius Standards:**
- **Small/Inside Elements**: Use `rounded-[0.75rem]` (0.75rem) for inner and small elements: buttons, inputs, dropdown items, avatars, standalone icon containers, ...
- **Large/Outside Elements**: Use `rounded-[1rem]` (1rem) for outer and big elements: boxes, page containers, major sections, content boxes, containers
- **Consistency**: Never use other radius values without explicit design system approval

**Three-Column Layout System:**
- **ThreeColumnLayout**: Use `@/widgets/three-column-layout` for flexible 3-column layouts
- **Adaptive Columns**: Layout automatically adjusts based on which sidebars are provided
- **Sidebar Widgets**: Reusable sidebar components in `@/widgets/*-sidebar/` using `SidebarCard` for consistent functionality
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
- **All Sidebars**: Use `SidebarCard` component with `sticky top-20` positioning to avoid header overlap

**SidebarCard Component:**
- **Unified Sidebar Interface**: All sidebar widgets MUST use `SidebarCard` from `@/shared/ui/sidebar-card` for consistent styling and behavior
- **Optional Header**: Title displays only when specified via `title` prop; when provided, shows with optional `icon` prop (icon size 20px)
- **Header Pattern**: Use `<IconComponent size={20} />` with semantic icons for each sidebar type
- **Content Spacing**: Control internal spacing with `contentSpacing` prop - `"sm"` (space-y-4), `"default"` (space-y-6), `"lg"` (space-y-8)
- **No Manual Headers**: Never manually implement `<div className="flex items-center gap-2">` headers - use SidebarCard props
- **Import**: `import { SidebarCard } from '@/shared/ui/sidebar-card'`

**Sidebar & Layout Elements:**
- **Box Wrapping**: Wrap sidebar elements (categories, filters, author info, etc.) in `Box` containers
- **Logical Grouping**: Each functional group gets its own box (e.g., separate boxes for categories, filters, actions)
- **Hierarchy**: Use box size variants to establish visual hierarchy (larger boxes for primary content)

**When to Use PageHeader:**
- **Always Required**: Every page (`/posts`, `/space`, `/hub`, `/catalog`, admin pages)
- **Demo Components**: Use `PageHeader` for all demo component headers
- **Content Sections**: Any section that has title + description should use PageHeader
- **Never Use**: Custom `<header>`, standalone `<h1>` when PageHeader should be used

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

// Good: Default muted icon container for neutral elements
<div className="bg-muted text-muted-foreground w-10 h-10 rounded-[0.75rem] flex items-center justify-center">
  <UserIcon size={20} />
</div>

// Good: Interactive button - icon color matches text, responsive text hiding
<IconButton
  icon={<AddIcon size={16} />}
  variant="success"
  responsive={true}
>
  Add
</IconButton>

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

// Good: SidebarCard with title and icon
<SidebarCard
  title={t('filters')}
  icon={<FilterIcon size={20} />}
  contentSpacing="default"
>
  <div className="space-y-6">
    {/* Your sidebar content */}
  </div>
</SidebarCard>

// Good: SidebarCard without header (admin navigation)
<SidebarCard contentSpacing="sm">
  <div className="space-y-1">
    {menuItems.map((item) => (
      <Button key={item.key} variant="ghost" className="w-full justify-start">
        {item.icon}
        {item.label}
      </Button>
    ))}
  </div>
</SidebarCard>

// Good: SectionsSidebar with optional title and icon
<SectionsSidebar
  title={t('businessSections')}
  icon={<BuildingIcon size={20} />}
/>

// Good: SectionsSidebar without title (clean navigation)
<SectionsSidebar />
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
1. **Follow Frontend Development Flow (UltraThink)**: Use the 5-step systematic flow for ALL frontend code
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
- **SidebarCard**: `import { SidebarCard } from '@/shared/ui/sidebar-card'` - Unified sidebar component with optional header (icon + title) and content spacing control
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
