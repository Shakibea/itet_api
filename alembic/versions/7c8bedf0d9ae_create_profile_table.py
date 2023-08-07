"""create profile table

Revision ID: 7c8bedf0d9ae
Revises: 5bdf4ba1ef89
Create Date: 2023-08-08 03:59:07.556501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c8bedf0d9ae'
down_revision = '5bdf4ba1ef89'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('membership_id', sa.Integer(), nullable=False),
    sa.Column('membership_status', sa.String(), nullable=True),
    sa.Column('batch_no', sa.Integer(), nullable=False),
    sa.Column('contact_no', sa.String(), nullable=True),
    sa.Column('dob', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('birth_place', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('present_address', sa.String(), nullable=True),
    sa.Column('permanent_address', sa.String(), nullable=True),
    sa.Column('blood_group', sa.String(), nullable=True),
    sa.Column('spouse_name', sa.String(), nullable=True),
    sa.Column('wedding_anniversary', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('about', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('membership_id')
    )
    op.create_index(op.f('ix_profile_id'), 'profile', ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_index(op.f('ix_profile_id'), table_name='profile')
    op.drop_table('profile')
    # ### end Alembic commands ###
