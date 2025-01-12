"""login jwt

Revision ID: 4d4f02247829
Revises: c6bcf8f4572c
Create Date: 2025-01-07 21:47:50.141152

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d4f02247829'
down_revision: Union[str, None] = 'c6bcf8f4572c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blocked_token',
    sa.Column('token_id', sa.String(length=255), nullable=False),
    sa.Column('expired_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('token_id')
    )
    op.add_column('user', sa.Column('nickname', sa.String(length=20), nullable=True))
    op.create_index(op.f('ix_user_nickname'), 'user', ['nickname'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_nickname'), table_name='user')
    op.drop_column('user', 'nickname')
    op.drop_table('blocked_token')
    # ### end Alembic commands ###
