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
- **Base URL**: API routes via nginx proxy at `http://localhost/api/`
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
- **API Access**: Backend API available at `http://localhost/api/` when containers are running
- **Port Mapping**: Frontend (Next.js) → nginx:80 → api:5000 (internal Docker network)
- **Direct API Testing**: Use curl commands in "API Testing & Development" section

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
