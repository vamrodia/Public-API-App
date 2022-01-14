"""create posts table

Revision ID: d8d8eb55a858
Revises: 
Create Date: 2022-01-13 16:30:55.705377

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8d8eb55a858'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
                    , sa.Column('title', sa.String(1000), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
