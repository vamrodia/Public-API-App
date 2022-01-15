"""add users  table

Revision ID: 566aad8fe8b7
Revises: 3c75192dca14
Create Date: 2022-01-14 16:55:29.824098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '566aad8fe8b7'
down_revision = '3c75192dca14'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(100), nullable=False),
                    sa.Column('password', sa.String(100), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
