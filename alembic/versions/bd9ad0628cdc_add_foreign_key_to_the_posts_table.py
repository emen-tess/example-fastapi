"""add foreign-key to the posts table

Revision ID: bd9ad0628cdc
Revises: 9b7a5bf219fd
Create Date: 2023-07-07 18:35:18.529253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd9ad0628cdc'
down_revision = '9b7a5bf219fd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('owner_id', sa.Integer, nullable=False))
    
    op.create_foreign_key('posts_users_fk', 
                          source_table="posts", 
                          referent_table="users",
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
