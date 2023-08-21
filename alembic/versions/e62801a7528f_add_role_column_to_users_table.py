"""add role column to users table

Revision ID: e62801a7528f
Revises: 7c8bedf0d9ae
Create Date: 2023-08-08 16:52:31.250207

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e62801a7528f'
down_revision = '7c8bedf0d9ae'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column(table_name='users', column_name='role')
    pass
