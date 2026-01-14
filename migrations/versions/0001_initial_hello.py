"""Create hello table.

Revision ID: 0001_initial_hello
Revises:
Create Date: 2025-02-06 00:00:00
"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_initial_hello"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "hello",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.Column("msg", sa.Text(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("hello")
