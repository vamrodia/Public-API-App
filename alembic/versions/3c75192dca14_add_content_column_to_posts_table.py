"""add content column to posts table

Revision ID: 3c75192dca14
Revises: 744306d820ef
Create Date: 2022-01-14 16:52:09.882129

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c75192dca14'
down_revision = '744306d820ef'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
