"""create events table

Revision ID: 5bdf4ba1ef89
Revises: 3c50ebcf9dbe
Create Date: 2023-08-07 18:52:37.157213

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5bdf4ba1ef89'
down_revision = '3c50ebcf9dbe'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('events',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False),
                    sa.Column('published', sa.Boolean(), server_default='True', nullable=False),
                    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('event_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('expire_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_events_id'), 'events', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_index(op.f('ix_events_id'), table_name='events')
    op.drop_table('events')
    # ### end Alembic commands ###
