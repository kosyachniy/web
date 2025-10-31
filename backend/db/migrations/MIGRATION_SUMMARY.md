# Database Migration Update Summary

## Overview
Complete database migration restructure with support for multiple user roles and proper table organization.

---

## 📋 What Was Changed

### 1. Migration Structure

**Old Structure:**
```
001_create_users_table.py
  ├─ users table (with single role field)
  ├─ posts table
  ├─ user_login_activities table
  └─ All ENUM types mixed together
```

**New Structure:**
```
001_create_users_table.py
  ├─ users table (with roles array field)
  ├─ user_login_activities table
  └─ User-related ENUM types: userrole, userstatus, authprovider

002_create_posts_and_content_tables.py
  ├─ categories table
  ├─ posts table
  ├─ comments table
  ├─ reactions table
  └─ Content-related ENUM types: poststatus, postvisibility, reactiontype
```

---

### 2. Users Table - Multiple Roles Support

**Before:**
```sql
role VARCHAR(50) NOT NULL DEFAULT 'user'
-- User could have only ONE role
```

**After:**
```sql
roles VARCHAR(50)[] NOT NULL DEFAULT ARRAY['USER']::userrole[]
-- User can have MULTIPLE roles
```

**Key Changes:**
- Field name: `role` → `roles` (singular to plural)
- Data type: `VARCHAR(50)` → `VARCHAR(50)[]` (array)
- Default value: `'USER'` → `ARRAY['USER']::userrole[]`
- Index: Created GIN index for efficient array queries

**Benefits:**
- ✅ Users can have multiple roles: `['USER', 'EDITOR', 'MODERATOR']`
- ✅ Fine-grained permission control
- ✅ Role-based access control (RBAC) with role combinations
- ✅ Efficient queries: `WHERE 'ADMIN' = ANY(roles)`

---

### 3. Database Schema Changes

#### Users Table (Migration 001)
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(320),
    phone VARCHAR(32),
    username VARCHAR(64),
    hashed_password TEXT,
    password_salt BYTEA,
    roles userrole[] NOT NULL DEFAULT ARRAY['USER']::userrole[],  -- ⭐ NEW
    status userstatus NOT NULL DEFAULT 'PENDING',
    is_email_verified BOOLEAN DEFAULT FALSE,
    is_phone_verified BOOLEAN DEFAULT FALSE,
    profile JSONB DEFAULT '{}'::jsonb,
    settings JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ⭐ NEW: GIN index for roles array queries
CREATE INDEX ix_users_roles ON users USING GIN (roles);
```

#### Categories Table (Migration 002)
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    parent_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    icon VARCHAR(50),
    color VARCHAR(20),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

#### Posts Table (Migration 002)
```sql
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    title VARCHAR(255) NOT NULL,
    summary VARCHAR(512),
    content TEXT NOT NULL,
    status poststatus DEFAULT 'DRAFT',
    visibility postvisibility DEFAULT 'PUBLIC',
    locale VARCHAR(10) DEFAULT 'en',
    seo JSONB DEFAULT '{}'::jsonb,
    extra JSONB DEFAULT '{}'::jsonb,
    is_featured BOOLEAN DEFAULT FALSE,
    view_count INTEGER DEFAULT 0,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

#### Comments Table (Migration 002)
```sql
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    author_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parent_id INTEGER REFERENCES comments(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    is_edited BOOLEAN DEFAULT FALSE,
    is_deleted BOOLEAN DEFAULT FALSE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

#### Reactions Table (Migration 002)
```sql
CREATE TABLE reactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    comment_id INTEGER REFERENCES comments(id) ON DELETE CASCADE,
    reaction_type reactiontype NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, post_id),
    UNIQUE (user_id, comment_id),
    CHECK (
        (post_id IS NOT NULL AND comment_id IS NULL) OR
        (post_id IS NULL AND comment_id IS NOT NULL)
    )
);
```

---

### 4. Code Changes

#### Domain Entity (`backend/app/domain/entities/user.py`)
```python
# Before
role: UserRole = Field(default=UserRole.USER)

# After
roles: list[UserRole] = Field(default=[UserRole.USER])

# New Methods
def add_role(self, role: UserRole) -> None:
    """Add a role to user."""
    if role not in self.roles:
        self.roles.append(role)
        self.mark_updated()

def remove_role(self, role: UserRole) -> None:
    """Remove a role from user."""
    if role in self.roles:
        self.roles.remove(role)
        if not self.roles:
            self.roles = [UserRole.USER]  # Always keep at least USER
        self.mark_updated()

def has_role(self, role: UserRole) -> bool:
    """Check if user has a specific role."""
    return role in self.roles

# Updated Property
@property
def is_admin(self) -> bool:
    """Check if user has admin privileges."""
    return UserRole.ADMIN in self.roles or UserRole.SUPER_ADMIN in self.roles
```

#### SQLAlchemy Model (`backend/app/adapters/database/postgres/models/user.py`)
```python
# Before
role: Mapped[str] = mapped_column(String(50), default="user")

# After
roles: Mapped[list[str]] = mapped_column(
    PG_ARRAY(String(50)),
    default=["user"],
    nullable=False,
    doc="User roles (multiple roles supported)"
)
```

#### API Schema (`backend/app/api/schemas/user.py`)
```python
# Before
role: str = Field(description="User role")

# After
roles: list[str] = Field(description="User roles (multiple roles supported)")
```

#### Permission Service (`backend/app/services/permissions.py`)
```python
# Before
async def has_permission(self, user: User, permission: str) -> bool:
    allowed = ROLE_HIERARCHY.get(user.role, set())
    return "*" in allowed or permission in allowed

# After
async def has_permission(self, user: User, permission: str) -> bool:
    """Check if user has permission based on their roles."""
    # Check permissions for all user roles
    for role in user.roles:
        allowed = ROLE_HIERARCHY.get(role, set())
        if "*" in allowed or permission in allowed:
            return True
    return False
```

---

### 5. ENUM Types

#### User-Related ENUMs (Migration 001)
```sql
-- User Roles
CREATE TYPE userrole AS ENUM (
    'SUPERADMIN',
    'ADMIN',
    'EDITOR',
    'CREATOR',
    'USER',
    'RESTRICTED'
);

-- User Status
CREATE TYPE userstatus AS ENUM (
    'ACTIVE',
    'PENDING',
    'BLOCKED',
    'DELETED'
);

-- Authentication Providers
CREATE TYPE authprovider AS ENUM (
    'PASSWORD',
    'GOOGLE',
    'GITHUB',
    'APPLE',
    'TELEGRAM',
    'PHONE'
);
```

#### Content-Related ENUMs (Migration 002)
```sql
-- Post Status
CREATE TYPE poststatus AS ENUM (
    'DRAFT',
    'PUBLISHED',
    'ARCHIVED'
);

-- Post Visibility
CREATE TYPE postvisibility AS ENUM (
    'PUBLIC',
    'PRIVATE',
    'UNLISTED'
);

-- Reaction Types
CREATE TYPE reactiontype AS ENUM (
    'LIKE',
    'LOVE',
    'DISLIKE',
    'FIRE',
    'STAR'
);
```

---

## 🔧 Migration Safety Features

### 1. Idempotent Type Creation
```python
def upgrade() -> None:
    # Drop existing types if they exist (cleanup from old migrations)
    op.execute("DROP TYPE IF EXISTS userrole CASCADE")
    op.execute("DROP TYPE IF EXISTS userstatus CASCADE")
    # ... then create fresh
```

### 2. Proper Cleanup in Downgrade
```python
def downgrade() -> None:
    op.drop_table("user_login_activities")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS authprovider CASCADE")
    op.execute("DROP TYPE IF EXISTS userrole CASCADE")
    op.execute("DROP TYPE IF EXISTS userstatus CASCADE")
```

### 3. Foreign Key Constraints
- `ON DELETE CASCADE`: Auto-delete child records
- `ON DELETE SET NULL`: Set foreign key to NULL
- Prevents orphaned records

### 4. Database Indexes
- Primary keys on all tables
- Unique indexes on `email`, `username`, `slug`
- Composite indexes for common queries
- GIN index on roles array for efficient searches

---

## 📦 Files Created/Modified

### New Files
```
✅ backend/migrations/versions/002_create_posts_and_content_tables.py
✅ backend/scripts/reset_database.py
✅ backend/scripts/reset_db.sh
✅ backend/scripts/cleanup_db.sql
✅ backend/migrations/RESET_GUIDE.md
✅ backend/migrations/MIGRATION_SUMMARY.md
✅ backend/QUICK_RESET.txt
```

### Modified Files
```
✏️  backend/migrations/versions/001_create_users_table.py
✏️  backend/app/domain/entities/user.py
✏️  backend/app/adapters/database/postgres/models/user.py
✏️  backend/app/api/schemas/user.py
✏️  backend/app/services/permissions.py
✏️  backend/tests/unit/test_user_entity.py
✏️  backend/tests/integration/test_database.py
```

---

## 🚀 How to Apply

### Option 1: Docker (Recommended)
```bash
# Reset database
docker compose exec api alembic downgrade base
docker compose exec api alembic upgrade head

# Restart services
docker compose restart api
```

### Option 2: Using Reset Script
```bash
cd backend
chmod +x scripts/reset_db.sh
./scripts/reset_db.sh
```

### Option 3: Manual SQL + Alembic
```bash
# Run cleanup SQL
cat backend/scripts/cleanup_db.sql | docker compose exec -T postgres psql -U postgres -d your_db

# Apply migrations
docker compose exec api alembic upgrade head
```

For detailed instructions, see: **`backend/QUICK_RESET.txt`**

---

## ✅ Verification

After applying migrations, verify:

```bash
# Check migration state
docker compose exec api alembic current
# Expected output: 0002 (head)

# View migration history
docker compose exec api alembic history
# Should show both 001 and 002 migrations

# Connect to database and verify
docker compose exec postgres psql -U postgres -d your_db
\dt  # List tables (should see users, posts, categories, comments, reactions)
\dT+ # List types (should see all ENUM types)
\d users  # Describe users table (should see roles as array)
```

---

## 📖 Usage Examples

### Creating Users with Multiple Roles
```python
# Single role (default)
user = User(
    email="user@example.com",
    username="john",
    password_hash="...",
    roles=[UserRole.USER]
)

# Multiple roles
admin_editor = User(
    email="admin@example.com",
    username="admin",
    password_hash="...",
    roles=[UserRole.ADMIN, UserRole.EDITOR, UserRole.MODERATOR]
)
```

### Managing Roles
```python
# Add a role
user.add_role(UserRole.EDITOR)

# Remove a role
user.remove_role(UserRole.EDITOR)

# Check if user has role
if user.has_role(UserRole.ADMIN):
    # Allow admin action
    pass

# Check admin privileges (ADMIN or SUPER_ADMIN)
if user.is_admin:
    # Allow admin/super-admin action
    pass
```

### Querying Users by Role
```sql
-- Find all admins
SELECT * FROM users WHERE 'ADMIN' = ANY(roles);

-- Find users with multiple specific roles
SELECT * FROM users WHERE roles @> ARRAY['USER', 'EDITOR']::userrole[];

-- Find users with any of these roles
SELECT * FROM users WHERE roles && ARRAY['ADMIN', 'MODERATOR']::userrole[];
```

---

## 🎯 Benefits

1. **Flexible Permissions**: Users can have multiple roles simultaneously
2. **Organized Migrations**: Logical separation of user auth and content tables
3. **Clean Schema**: Proper foreign keys, constraints, and indexes
4. **Type Safety**: PostgreSQL ENUMs ensure data integrity
5. **Scalability**: GIN indexes for efficient role-based queries
6. **Maintainability**: Clear migration structure and documentation

---

## 🔍 Troubleshooting

See **`backend/migrations/RESET_GUIDE.md`** for:
- Common errors and solutions
- Step-by-step reset procedures
- Best practices for migrations
- Development workflow tips

---

## 📚 References

- [PostgreSQL ARRAY Data Type](https://www.postgresql.org/docs/current/arrays.html)
- [GIN Indexes](https://www.postgresql.org/docs/current/gin.html)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)

---

**Migration completed successfully! ✨**

If you encounter any issues, refer to:
- `backend/QUICK_RESET.txt` - Quick command reference
- `backend/migrations/RESET_GUIDE.md` - Detailed guide
- `backend/scripts/cleanup_db.sql` - Manual cleanup script
