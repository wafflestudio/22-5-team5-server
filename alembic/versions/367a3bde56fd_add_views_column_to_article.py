"""Add views column to Article

Revision ID: 367a3bde56fd
Revises: c7b0dc7d783d
Create Date: 2025-01-19 04:46:14.657790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '367a3bde56fd'
down_revision: Union[str, None] = 'c7b0dc7d783d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Article', sa.Column('views', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Article', 'views')
    # ### end Alembic commands ###
