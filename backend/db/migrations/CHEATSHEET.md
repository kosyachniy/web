# Migration Cheat Sheet

## 🚀 Quick Commands

### Reset Database (Choose One)

```bash
# 1. Docker One-Liner (FASTEST)
docker compose exec api alembic downgrade base && docker compose exec api alembic upgrade head

# 2. SQL Cleanup + Migrate
cat backend/scripts/cleanup_db.sql | docker compose exec -T postgres psql -U postgres -d your_db_name
docker compose exec api alembic upgrade head

# 3. Shell Script
cd backend && chmod +x scripts/reset_db.sh && ./scripts/reset_db.sh

# 4. Python Script
cd backend && python scripts/reset_database.py && alembic upgrade head
```

---

## 📊 Migration Status

```bash
# Current migration
docker compose exec api alembic current

# Migration history
docker compose exec api alembic history

# View SQL without executing
docker compose exec api alembic upgrade head --sql
```

---

## 🔄 Migration Operations

```bash
# Upgrade to latest
alembic upgrade head

# Downgrade one step
alembic downgrade -1

# Downgrade to base (remove all)
alembic downgrade base

# Upgrade to specific revision
alembic upgrade <revision_id>
```

---

## 🔍 Database Inspection

```bash
# Connect to database
docker compose exec postgres psql -U postgres -d your_db_name

# Inside psql:
\dt              # List all tables
\dT+             # List all types (ENUMs)
\d users         # Describe users table
\d+ posts        # Detailed description of posts table
\di              # List all indexes
\q               # Quit psql
```

---

## 👤 Roles Usage (Python)

```python
from app.domain.entities.user import User, UserRole

# Create user with roles
user = User(
    email="user@example.com",
    username="john",
    password_hash="...",
    roles=[UserRole.USER, UserRole.EDITOR]  # Multiple roles
)

# Manage roles
user.add_role(UserRole.MODERATOR)          # Add role
user.remove_role(UserRole.EDITOR)          # Remove role
has_admin = user.has_role(UserRole.ADMIN)  # Check role
is_admin = user.is_admin                   # Admin check (ADMIN or SUPER_ADMIN)

# Available roles
UserRole.SUPERADMIN
UserRole.ADMIN
UserRole.EDITOR
UserRole.CREATOR
UserRole.USER
UserRole.RESTRICTED
```

---

## 🗄️ SQL Queries (PostgreSQL Arrays)

```sql
-- Find users with specific role
SELECT * FROM users WHERE 'ADMIN' = ANY(roles);

-- Find users with ALL specified roles
SELECT * FROM users WHERE roles @> ARRAY['USER', 'EDITOR']::userrole[];

-- Find users with ANY of specified roles
SELECT * FROM users WHERE roles && ARRAY['ADMIN', 'MODERATOR']::userrole[];

-- Find users without a role
SELECT * FROM users WHERE NOT ('RESTRICTED' = ANY(roles));

-- Count users by role
SELECT UNNEST(roles) AS role, COUNT(*) FROM users GROUP BY role;
```

---

## 🗂️ Table Structure Quick Reference

### Users (Migration 001)
```
id, email, phone, username, hashed_password, password_salt,
roles[], status, is_email_verified, is_phone_verified,
profile, settings, created_at, updated_at
```

### Categories (Migration 002)
```
id, name, slug, description, parent_id, icon, color,
sort_order, is_active, metadata, created_at, updated_at
```

### Posts (Migration 002)
```
id, author_id, category_id, slug, title, summary, content,
status, visibility, locale, seo, extra, is_featured,
view_count, published_at, created_at, updated_at
```

### Comments (Migration 002)
```
id, post_id, author_id, parent_id, content, is_edited,
is_deleted, metadata, created_at, updated_at
```

### Reactions (Migration 002)
```
id, user_id, post_id, comment_id, reaction_type, created_at
```

---

## 📝 Creating New Migrations

```bash
# Auto-generate from model changes
alembic revision --autogenerate -m "Add new feature"

# Create blank migration
alembic revision -m "Custom migration"

# Edit the generated file in: backend/migrations/versions/

# Apply the migration
alembic upgrade head
```

---

## ⚠️ Common Errors & Fixes

| Error | Solution |
|-------|----------|
| `type already exists` | Run `cleanup_db.sql` then migrate |
| `relation already exists` | Downgrade to base: `alembic downgrade base` |
| `cannot drop type ... depends` | Use `DROP TYPE ... CASCADE` |
| `alembic_version not found` | Normal on first run, just run `upgrade head` |

---

## 🎯 Key Changes Summary

### Before
- `role VARCHAR(50)` - Single role only
- All tables in one migration

### After
- `roles VARCHAR(50)[]` - Array of roles ✨
- Two logical migrations (001: users, 002: content)
- GIN indexes for array queries
- Proper foreign keys with CASCADE

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `QUICK_RESET.txt` | Quick command reference (this file) |
| `RESET_GUIDE.md` | Detailed reset procedures |
| `MIGRATION_SUMMARY.md` | Complete changelog |
| `CHEATSHEET.md` | Common operations reference |
| `cleanup_db.sql` | SQL cleanup script |
| `reset_database.py` | Python reset script |
| `reset_db.sh` | Bash reset script |

---

## 🔗 Quick Links

```bash
# View all docs
ls -la backend/migrations/*.md
ls -la backend/scripts/

# Read specific doc
cat backend/QUICK_RESET.txt
cat backend/migrations/RESET_GUIDE.md
cat backend/migrations/MIGRATION_SUMMARY.md
```

---

**Pro Tips:**

1. Always backup production before migrations: `pg_dump -U postgres your_db > backup.sql`
2. Test migrations in development first
3. Use `--sql` flag to preview SQL before applying
4. Keep migrations small and focused
5. Document complex migrations in comments

---

**Need Help?**

- Read: `backend/migrations/RESET_GUIDE.md`
- Check logs: `docker compose logs api`
- Verify DB connection: `docker compose ps postgres`
- Test connection: `docker compose exec postgres psql -U postgres -c "SELECT version()"`
