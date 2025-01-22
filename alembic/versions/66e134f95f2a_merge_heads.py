"""merge heads

Revision ID: 66e134f95f2a
Revises: a4ec916e0932, eadc58f31090
Create Date: 2025-01-23 00:29:45.607325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66e134f95f2a'
down_revision: Union[str, None] = 'a4ec916e0932'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
