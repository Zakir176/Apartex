"""v2_phase0_property_model_walkin_fields

Revision ID: a45c016ae33d
Revises: 
Create Date: 2026-07-23 11:35:46.679838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a45c016ae33d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()

    # If database is completely empty (no tables), create all tables from Base metadata
    if not tables:
        from app.database import Base
        import app.models  # Ensure models are loaded
        Base.metadata.create_all(bind=conn)
        inspector = sa.inspect(conn)
        tables = inspector.get_table_names()

    # 1. Rename apartments table to properties if apartments exists
    if "apartments" in tables and "properties" not in tables:
        op.rename_table("apartments", "properties")

    # 2. Add property_type and star_rating to properties table if needed
    if "properties" in op.get_bind().dialect.get_table_names(op.get_bind()):
        columns = [c["name"] for c in sa.inspect(op.get_bind()).get_columns("properties")]
        with op.batch_alter_table("properties") as batch_op:
            if "property_type" not in columns:
                batch_op.add_column(sa.Column("property_type", sa.String(length=20), nullable=False, server_default="apartment"))
            if "star_rating" not in columns:
                batch_op.add_column(sa.Column("star_rating", sa.Integer(), nullable=True))

    # 3. Update bookings table (rename apartment_id to property_id and add walk-in fields)
    if "bookings" in op.get_bind().dialect.get_table_names(op.get_bind()):
        columns = [c["name"] for c in sa.inspect(op.get_bind()).get_columns("bookings")]
        with op.batch_alter_table("bookings") as batch_op:
            if "apartment_id" in columns and "property_id" not in columns:
                batch_op.alter_column("apartment_id", new_column_name="property_id", existing_type=sa.Integer())
            if "is_walk_in" not in columns:
                batch_op.add_column(sa.Column("is_walk_in", sa.Boolean(), nullable=False, server_default=sa.text("0")))
            if "payment_method" not in columns:
                batch_op.add_column(sa.Column("payment_method", sa.String(length=50), nullable=True))
            if "walk_in_guest_name" not in columns:
                batch_op.add_column(sa.Column("walk_in_guest_name", sa.String(length=200), nullable=True))
            if "walk_in_guest_phone" not in columns:
                batch_op.add_column(sa.Column("walk_in_guest_phone", sa.String(length=50), nullable=True))
            if "created_by_owner" not in columns:
                batch_op.add_column(sa.Column("created_by_owner", sa.Boolean(), nullable=False, server_default=sa.text("0")))


def downgrade() -> None:
    """Downgrade schema."""
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()

    if "bookings" in tables:
        columns = [c["name"] for c in inspector.get_columns("bookings")]
        with op.batch_alter_table("bookings") as batch_op:
            if "created_by_owner" in columns:
                batch_op.drop_column("created_by_owner")
            if "walk_in_guest_phone" in columns:
                batch_op.drop_column("walk_in_guest_phone")
            if "walk_in_guest_name" in columns:
                batch_op.drop_column("walk_in_guest_name")
            if "payment_method" in columns:
                batch_op.drop_column("payment_method")
            if "is_walk_in" in columns:
                batch_op.drop_column("is_walk_in")
            if "property_id" in columns and "apartment_id" not in columns:
                batch_op.alter_column("property_id", new_column_name="apartment_id", existing_type=sa.Integer())

    if "properties" in tables:
        columns = [c["name"] for c in inspector.get_columns("properties")]
        with op.batch_alter_table("properties") as batch_op:
            if "star_rating" in columns:
                batch_op.drop_column("star_rating")
            if "property_type" in columns:
                batch_op.drop_column("property_type")

        if "apartments" not in tables:
            op.rename_table("properties", "apartments")


