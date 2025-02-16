"""Update JournalEntry - project_id nullable

Revision ID: da48d6fc6d46
Revises: e9b034e6da40
Create Date: 2025-02-15 23:49:20.776170

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision: str = "da48d6fc6d46"
down_revision: Union[str, None] = "e9b034e6da40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create new table with desired schema
    with op.batch_alter_table("journal_entry") as batch_op:
        batch_op.alter_column("project_id", existing_type=sa.VARCHAR(), nullable=True)


def downgrade() -> None:
    # Revert changes
    with op.batch_alter_table("journal_entry") as batch_op:
        batch_op.alter_column("project_id", existing_type=sa.VARCHAR(), nullable=False)
