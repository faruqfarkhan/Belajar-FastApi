"""add last few column to posts table

Revision ID: 8b566028b7a5
Revises: c54a169d2e11
Create Date: 2024-11-06 19:01:13.541380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b566028b7a5'
down_revision: Union[str, None] = 'c54a169d2e11'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE")),
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True),nullable=False,
                   server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column("posts", "created_at"),
    op.drop_column("posts", "published")

