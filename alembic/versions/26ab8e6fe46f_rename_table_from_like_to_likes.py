"""Rename table from like to likes

Revision ID: 26ab8e6fe46f
Revises: bd24e27678f8
Create Date: 2025-01-16 01:19:27.361173

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '26ab8e6fe46f'
down_revision: Union[str, None] = 'bd24e27678f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_like',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('blog_id', sa.BigInteger(), nullable=False),
    sa.Column('article_id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['Article.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['blog_id'], ['blog.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('like')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('like',
    sa.Column('id', mysql.BIGINT(), autoincrement=True, nullable=False),
    sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('blog_id', mysql.BIGINT(), autoincrement=False, nullable=False),
    sa.Column('article_id', mysql.BIGINT(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['article_id'], ['Article.id'], name='like_ibfk_1', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['blog_id'], ['blog.id'], name='like_ibfk_2', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('blog_like')
    # ### end Alembic commands ###