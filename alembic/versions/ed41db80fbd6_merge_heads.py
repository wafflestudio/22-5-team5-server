"""merge heads

Revision ID: ed41db80fbd6
Revises: 6d917caae9a0, ca2911583c0f
Create Date: 2025-01-21 00:14:59.319725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed41db80fbd6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
