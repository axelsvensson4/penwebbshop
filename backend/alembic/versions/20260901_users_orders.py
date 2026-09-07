"""Create users, sessions and orders tables.

Revision ID: 20260901_users_orders
"""

revision = '20260901_users_orders'
down_revision = None


def upgrade() -> None:
    """Schema is also initialized by app.database for this SQLite demo."""


def downgrade() -> None:
    """Intentionally empty: use an explicit migration before production."""
