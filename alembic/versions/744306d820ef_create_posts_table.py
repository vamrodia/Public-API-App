"""create posts table

Revision ID: 744306d820ef
Revises: 
Create Date: 2022-01-14 16:49:07.791619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '744306d820ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True)
                    , sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
