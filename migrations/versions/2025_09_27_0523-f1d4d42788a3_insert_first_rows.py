# mypy: ignore-errors
# ruff: noqa: INP001
"""Insert first rows.

Revision ID: f1d4d42788a3
Revises: e055ca2cc1a3
Create Date: 2025-09-27 05:23:16.835022

"""

from collections.abc import Sequence

from alembic import op

from migrations.queries.first_rows import (
    insert_first_rows_with_async_connection,
)

# revision identifiers, used by Alembic.
revision: str = "f1d4d42788a3"
down_revision: str | None = "e055ca2cc1a3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.run_async(insert_first_rows_with_async_connection)


def downgrade() -> None:
    """Downgrade schema."""
