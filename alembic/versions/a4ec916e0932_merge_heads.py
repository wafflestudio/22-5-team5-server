"""merge heads

Revision ID: a4ec916e0932
Revises: 6d917caae9a0, 9741662cd9a8
Create Date: 2025-01-23 00:29:25.119942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4ec916e0932'
down_revision: Union[str, None] = ('6d917caae9a0', '9741662cd9a8')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
