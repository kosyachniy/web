"""Create users and authentication tables

Revision ID: 0001
Revises:
Create Date: 2024-05-08
"""

from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ENUM types for users
    op.execute("""
        CREATE TYPE userrole AS ENUM (
            'SUPERADMIN',
            'ADMIN',
            'EDITOR',
            'CREATOR',
            'USER',
            'RESTRICTED'
        )
    """)

    op.execute("""
        CREATE TYPE userstatus AS ENUM (
            'ACTIVE',
            'PENDING',
            'BLOCKED',
            'DELETED'
        )
    """)

    op.execute("""
        CREATE TYPE authprovider AS ENUM (
            'PASSWORD',
            'GOOGLE',
            'GITHUB',
            'APPLE',
            'TELEGRAM',
            'PHONE'
        )
    """)

    # Create users table with roles (plural, array)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=True),
        sa.Column("phone", sa.String(length=32), nullable=True),
        sa.Column("username", sa.String(length=64), nullable=True),
        sa.Column("hashed_password", sa.Text(), nullable=True),
        sa.Column("password_salt", sa.LargeBinary(), nullable=True),
        # Changed from singular role to plural roles (array)
        sa.Column(
            "roles",
            postgresql.ARRAY(sa.Enum("SUPERADMIN", "ADMIN", "EDITOR", "CREATOR", "USER", "RESTRICTED", name="userrole")),
            nullable=False,
            server_default=sa.text("ARRAY['USER']::userrole[]")
        ),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "PENDING", "BLOCKED", "DELETED", name="userstatus"),
            nullable=False,
            server_default="PENDING"
        ),
        sa.Column("is_email_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("is_phone_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("profile", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("settings", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes for users
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_phone"), "users", ["phone"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_index(op.f("ix_users_email_phone"), "users", ["email", "phone"], unique=False)

    # Create GIN index for roles array to optimize role-based queries
    op.create_index("ix_users_roles", "users", ["roles"], postgresql_using="gin")

    # Create user login activities table
    op.create_table(
        "user_login_activities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "provider",
            sa.Enum("PASSWORD", "GOOGLE", "GITHUB", "APPLE", "TELEGRAM", "PHONE", name="authprovider"),
            nullable=False
        ),
        sa.Column("ip_address", sa.String(length=64), nullable=True),
        sa.Column("user_agent", sa.String(length=255), nullable=True),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_login_activities_user_id"), "user_login_activities", ["user_id"], unique=False)
    op.create_index(op.f("ix_user_login_activities_created_at"), "user_login_activities", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_table("user_login_activities")
    op.drop_table("users")
    op.execute("DROP TYPE IF EXISTS authprovider")
    op.execute("DROP TYPE IF EXISTS userrole")
    op.execute("DROP TYPE IF EXISTS userstatus")
