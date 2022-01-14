"""add content column to posts table

Revision ID: 6a783a720a54
Revises: d8d8eb55a858
Create Date: 2022-01-13 22:23:22.681174

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a783a720a54'
down_revision = 'd8d8eb55a858'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(1000), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
