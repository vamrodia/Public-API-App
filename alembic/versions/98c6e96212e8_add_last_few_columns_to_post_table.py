"""add last few columns to  post table

Revision ID: 98c6e96212e8
Revises: 85b8b548bd79
Create Date: 2022-01-14 16:57:47.070372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98c6e96212e8'
down_revision = '85b8b548bd79'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='1'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False
                                     , server_default=sa.text('NOW()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
