"""create todo_lists table

Revision ID: cd7b780dca56
Revises:
Create Date: 2024-07-12 00:07:24.005239

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cd7b780dca56"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "todo_lists",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(50), nullable=False),
        sa.Column("description", sa.Unicode(200)),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
    )


def downgrade() -> None:
    op.drop_table("todo_lists")
