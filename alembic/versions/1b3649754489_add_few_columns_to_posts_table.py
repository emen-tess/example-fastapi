"""add few columns to posts table

Revision ID: 1b3649754489
Revises: bd9ad0628cdc
Create Date: 2023-07-07 18:53:56.851954

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b3649754489'
down_revision = 'bd9ad0628cdc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                    sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts',
                    sa.Column('created_at', sa.TIMESTAMP, nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
