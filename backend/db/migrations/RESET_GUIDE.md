# Database Migration Reset Guide

## Problem
The database has old migration artifacts (tables, ENUM types) that conflict with the new migration structure.

## Solution Options

Choose **one** of these methods to reset your database:

---

## Option 1: Quick Reset (Docker Environment)

If you're using Docker, this is the fastest way:

```bash
# From project root
docker compose down
docker compose up -d postgres redis mongodb  # Start only databases
docker compose exec api alembic downgrade base
docker compose exec api alembic upgrade head
docker compose up  # Start all services
```

---

## Option 2: Using Reset Script (Recommended)

```bash
# From backend directory
cd backend

# Make script executable (Linux/Mac)
chmod +x scripts/reset_db.sh

# Run the reset script
./scripts/reset_db.sh
```

This script will:
1. Downgrade all migrations to base
2. Run cleanup script (optional)
3. Upgrade to latest migrations
4. Verify final state

---

## Option 3: Manual Reset (Step-by-Step)

### Step 1: Connect to Database

**Via Docker:**
```bash
docker compose exec postgres psql -U postgres -d your_db_name
```

**Via psql directly:**
```bash
psql -U postgres -d your_db_name
```

### Step 2: Drop Everything

```sql
-- Drop all tables
DROP TABLE IF EXISTS reactions CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS user_login_activities CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS alembic_version CASCADE;

-- Drop all ENUM types
DROP TYPE IF EXISTS reactiontype CASCADE;
DROP TYPE IF EXISTS postvisibility CASCADE;
DROP TYPE IF EXISTS poststatus CASCADE;
DROP TYPE IF EXISTS authprovider CASCADE;
DROP TYPE IF EXISTS userstatus CASCADE;
DROP TYPE IF EXISTS userrole CASCADE;

-- Exit psql
\q
```

### Step 3: Apply Migrations

```bash
# From backend directory
cd backend

# Apply all migrations from scratch
alembic upgrade head

# Verify
alembic current
```

---

## Option 4: Python Reset Script

```bash
# From backend directory
cd backend

# Run the reset script
python scripts/reset_database.py

# Then apply migrations
alembic upgrade head
```

---

## Verification

After reset, verify the migration state:

```bash
# Check current migration version
alembic current

# Should show: 0002 (head)

# Check migration history
alembic history --verbose

# Should show:
# 0001 -> 0002 (head), Create posts, categories, comments, and reactions tables
# <base> -> 0001, Create users and authentication tables
```

---

## New Migration Structure

### Migration 001: Users & Authentication
- `users` table with **roles array** (PostgreSQL ARRAY type)
- `user_login_activities` table
- ENUM types: `userrole`, `userstatus`, `authprovider`

### Migration 002: Posts & Content
- `categories` table (hierarchical support)
- `posts` table (linked to users and categories)
- `comments` table (nested comments support)
- `reactions` table (for posts and comments)
- ENUM types: `poststatus`, `postvisibility`, `reactiontype`

---

## Key Changes

### ✅ What Changed

1. **Users.role → Users.roles**: Now supports multiple roles per user
   - Old: `role VARCHAR(50)` (single role)
   - New: `roles VARCHAR(50)[]` (array of roles)
   - Default: `ARRAY['USER']::userrole[]`

2. **Migration Split**: Separated into logical groups
   - 001: Users and authentication
   - 002: Posts, categories, comments, reactions

3. **ENUM Type Handling**: Now uses `DROP IF EXISTS CASCADE` before creation
   - Prevents conflicts with existing types
   - Clean migration from old structure

### ✅ Migration Safety

The migrations now include:
- `DROP TYPE IF EXISTS ... CASCADE` before creating types
- Proper foreign key constraints with CASCADE
- GIN indexes for array columns (roles)
- All timestamps with timezone support

---

## Troubleshooting

### Error: "type already exists"
- **Cause**: Old migration artifacts in database
- **Solution**: Use Option 1 or Option 3 (manual reset)

### Error: "relation already exists"
- **Cause**: Tables from old migrations
- **Solution**: Drop all tables manually (Option 3, Step 2)

### Error: "alembic_version table not found"
- **Cause**: Clean database (expected on first run)
- **Solution**: Just run `alembic upgrade head`

### Error: Migration fails mid-way
1. Check which migration failed: `alembic current`
2. Downgrade one step: `alembic downgrade -1`
3. Review error logs
4. Fix issue and retry: `alembic upgrade head`

---

## Best Practices

1. **Always backup production data** before migrations
2. **Test migrations** in development first
3. **Use transactions** (migrations run in transactions by default)
4. **Verify state** after migrations: `alembic current`
5. **Keep migrations small** and focused on specific changes

---

## Need Help?

If you encounter issues:

1. Check logs: `docker compose logs api` or application logs
2. Verify database connection settings in `.env`
3. Ensure PostgreSQL is running: `docker compose ps postgres`
4. Check migration files in `backend/migrations/versions/`

---

## Development Workflow

### Creating New Migrations

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "description"

# Create empty migration
alembic revision -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback all migrations
alembic downgrade base
```

### Testing Migrations

```bash
# Check migration without applying
alembic upgrade head --sql

# Test upgrade/downgrade cycle
alembic upgrade head
alembic downgrade base
alembic upgrade head
```

---

## Quick Reference

```bash
# Current state
alembic current

# Migration history
alembic history

# Upgrade to specific version
alembic upgrade <revision>

# Downgrade to specific version
alembic downgrade <revision>

# Show SQL without executing
alembic upgrade head --sql
```
