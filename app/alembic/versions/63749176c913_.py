"""empty message

Revision ID: 63749176c913
Revises: a25c2c8d8ddb
Create Date: 2024-11-06 18:38:10.346676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63749176c913'
down_revision: Union[str, None] = 'a25c2c8d8ddb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
