"""v2_phase1_room_model

Revision ID: 59a6df6e4e41
Revises: a45c016ae33d
Create Date: 2026-07-25 12:59:01.874867

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59a6df6e4e41'
down_revision: Union[str, Sequence[str], None] = 'a45c016ae33d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()

    if 'rooms' not in tables:
        op.create_table(
            'rooms',
            sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
            sa.Column('property_id', sa.Integer(), sa.ForeignKey('properties.id'), nullable=False),
            sa.Column('room_type', sa.String(length=100), nullable=False),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('price_per_night', sa.Numeric(precision=10, scale=2), nullable=False),
            sa.Column('capacity', sa.Integer(), nullable=False),
            sa.Column('total_units', sa.Integer(), nullable=False, server_default='1'),
            sa.Column('amenities', sa.Text(), nullable=True),
            sa.Column('image_url', sa.String(length=500), nullable=True),
            sa.Column('is_available', sa.Boolean(), server_default='1'),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True)
        )
        op.create_index(op.f('ix_rooms_id'), 'rooms', ['id'], unique=False)

    if 'bookings' in tables:
        booking_cols = [c['name'] for c in inspector.get_columns('bookings')]
        with op.batch_alter_table('bookings', schema=None) as batch_op:
            if 'room_id' not in booking_cols:
                batch_op.add_column(sa.Column('room_id', sa.Integer(), sa.ForeignKey('rooms.id'), nullable=True))
            batch_op.alter_column('user_id', existing_type=sa.INTEGER(), nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('bookings', schema=None) as batch_op:
        batch_op.alter_column('user_id', existing_type=sa.INTEGER(), nullable=False)
        batch_op.drop_column('room_id')
    op.drop_index(op.f('ix_rooms_id'), table_name='rooms')
    op.drop_table('rooms')
