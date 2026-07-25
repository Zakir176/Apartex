"""v2_phase1_room_model

Revision ID: b1c2d3e4f5a6
Revises: a45c016ae33d
Create Date: 2026-07-25 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'b1c2d3e4f5a6'
down_revision = 'a45c016ae33d'
branch_labels = None
depends_on = None

def upgrade() -> None:
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()

    if "rooms" not in tables:
        op.create_table(
            "rooms",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("property_id", sa.Integer(), sa.ForeignKey("properties.id"), nullable=False),
            sa.Column("room_type", sa.String(100), nullable=False),
            sa.Column("description", sa.Text(), nullable=True),
            sa.Column("price_per_night", sa.Numeric(10, 2), nullable=False),
            sa.Column("capacity", sa.Integer(), nullable=False),
            sa.Column("total_units", sa.Integer(), nullable=False, server_default="1"),
            sa.Column("amenities", sa.Text(), nullable=True),
            sa.Column("image_url", sa.String(500), nullable=True),
            sa.Column("is_available", sa.Boolean(), server_default=sa.text("1")),
            sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
            sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if "bookings" in tables:
        columns = [c["name"] for c in inspector.get_columns("bookings")]
        with op.batch_alter_table("bookings") as batch_op:
            if "room_id" not in columns:
                batch_op.add_column(sa.Column("room_id", sa.Integer(), nullable=True))
            if "user_id" in columns:
                batch_op.alter_column("user_id", existing_type=sa.Integer(), nullable=True)

def downgrade() -> None:
    op.drop_table("rooms")
