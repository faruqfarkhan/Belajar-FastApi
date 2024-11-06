"""create post table

Revision ID: a25c2c8d8ddb
Revises: 
Create Date: 2024-11-05 09:44:10.297588

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a25c2c8d8ddb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.create_table("posts", sa.Column('id', sa.Integer(), nullable=False,primary_key=True), sa.Column('title', sa.String(), nullable=False))

    pass


def downgrade():
    op.drop_table("posts")
    pass
