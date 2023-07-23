"""add content column to posts table

Revision ID: 911b89b2779e
Revises: 9063fce3ae67
Create Date: 2023-07-06 18:19:25.978221

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '911b89b2779e'
down_revision = '9063fce3ae67'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
