"""create todo_items table

Revision ID: 3f0b5fa5c5e1
Revises: cd7b780dca56
Create Date: 2024-07-27 05:19:27.137642

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3f0b5fa5c5e1"
down_revision: str | None = "cd7b780dca56"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "todo_items",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("todo_list_id", sa.Integer, nullable=False),
        sa.Column("title", sa.String(50), nullable=False),
        sa.Column("description", sa.Unicode(200)),
        sa.Column("status_code", sa.Integer, nullable=False),
        sa.Column("due_at", sa.DateTime),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["todo_list_id"], ["todo_lists.id"], name="todo_list_id_fk", ondelete="CASCADE"),
    )


def downgrade() -> None:
    op.drop_table("todo_items")
