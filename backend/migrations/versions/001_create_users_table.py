"""create_users_table

Revision ID: 001
Revises:
Create Date: 2024-09-16 18:04:00.000000

"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create users table with comprehensive fields and indexes."""
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('full_name', sa.String(100), nullable=True),
        sa.Column('password_hash', sa.String(128), nullable=False),
        sa.Column('status', sa.Integer(), nullable=False, default=1, comment='1=active, 0=inactive, -1=suspended'),
        sa.Column('role', sa.String(20), nullable=False, default='user', comment='user, admin, moderator'),
        sa.Column('email_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('phone_verified', sa.Boolean(), nullable=False, default=False),
        sa.Column('timezone', sa.String(50), nullable=False, default='UTC'),
        sa.Column('language', sa.String(10), nullable=False, default='en'),
        sa.Column('avatar_url', sa.String(500), nullable=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True, comment='Additional user data'),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_ip', sa.String(45), nullable=True),
        sa.Column('login_count', sa.Integer(), nullable=False, default=0),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=False, default=0),
        sa.Column('locked_until', sa.DateTime(timezone=True), nullable=True),
        sa.Column('password_changed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('terms_accepted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('privacy_accepted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('marketing_emails_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('notification_emails_enabled', sa.Boolean(), nullable=False, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, default=1, comment='Optimistic locking'),
    )

    # Primary indexes for performance
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_username', 'users', ['username'], unique=True)

    # Status and role indexes for filtering
    op.create_index('idx_users_status', 'users', ['status'])
    op.create_index('idx_users_role', 'users', ['role'])

    # Composite indexes for common queries
    op.create_index('idx_users_status_created', 'users', ['status', 'created_at'])
    op.create_index('idx_users_email_verified', 'users', ['email_verified'])

    # Soft delete index
    op.create_index('idx_users_deleted_at', 'users', ['deleted_at'])

    # Authentication indexes
    op.create_index('idx_users_last_login', 'users', ['last_login_at'])
    op.create_index('idx_users_locked_until', 'users', ['locked_until'])

    # Create constraints
    op.create_check_constraint(
        'check_users_status',
        'users',
        "status IN (-1, 0, 1)",
    )

    op.create_check_constraint(
        'check_users_role',
        'users',
        "role IN ('user', 'admin', 'moderator')",
    )

    op.create_check_constraint(
        'check_users_email_format',
        'users',
        "email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'",
    )


def downgrade() -> None:
    """Drop users table and all associated indexes."""
    op.drop_table('users')