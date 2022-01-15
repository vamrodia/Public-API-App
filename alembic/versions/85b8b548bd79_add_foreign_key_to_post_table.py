"""add foreign key to post table

Revision ID: 85b8b548bd79
Revises: 566aad8fe8b7
Create Date: 2022-01-14 16:56:41.350168

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85b8b548bd79'
down_revision = '566aad8fe8b7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users"
                          , local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
