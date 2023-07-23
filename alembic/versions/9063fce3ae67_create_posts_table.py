"""create posts table

Revision ID: 9063fce3ae67
Revises: 
Create Date: 2023-07-06 14:56:59.609711

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9063fce3ae67'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)) 
    pass


def downgrade() -> None:
    sa.drop_table('posts')
    pass

