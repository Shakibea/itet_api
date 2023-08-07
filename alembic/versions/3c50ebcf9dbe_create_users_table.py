"""create users table

Revision ID: 3c50ebcf9dbe
Revises: 
Create Date: 2023-08-07 18:25:38.205753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c50ebcf9dbe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, primary_key=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass


# ADD FOREIGN KEY COLUMN TO ANY TABLE

# def upgrade() -> None: op.add_column('events', sa.Column('owner_id', sa.Integer(), nullable=False))
# op.create_foreign_key('event_users_fk', source_table="events", referent_table="users", local_cols=['owner_id'],
# remote_cols=['id'], ondelete="CASCADE") pass
#
#
# def downgrade() -> None:
#     op.drop_constraint('post_users_fk', table_name='posts')
#     op.drop_column('posts', 'owner_id')
#     pass
