"""2024_08_07_61ee0ca

Revision ID: 620478159033
Revises: aef008d905da
Create Date: 2024-08-07 17:53:21.544663

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "620478159033"
down_revision: Union[str, None] = "aef008d905da"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("desc", sa.String(), nullable=True),
        sa.Column("room_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["room_id"], ["booking.rooms.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_images_id"), "images", ["id"], unique=True, schema="booking"
    )
    op.create_index(
        op.f("ix_booking_images_room_id"),
        "images",
        ["room_id"],
        unique=False,
        schema="booking",
    )
    op.add_column(
        "hotels",
        sa.Column("main_image_id", sa.Integer(), nullable=True),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_hotels_main_image_id"),
        "hotels",
        ["main_image_id"],
        unique=False,
        schema="booking",
    )
    op.create_foreign_key(
        None,
        "hotels",
        "images",
        ["main_image_id"],
        ["id"],
        source_schema="booking",
        referent_schema="booking",
        onupdate="CASCADE",
        ondelete="SET NULL",
    )
    op.add_column(
        "rooms",
        sa.Column("main_image_id", sa.Integer(), nullable=True),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_rooms_main_image_id"),
        "rooms",
        ["main_image_id"],
        unique=False,
        schema="booking",
    )
    op.create_foreign_key(
        None,
        "rooms",
        "images",
        ["main_image_id"],
        ["id"],
        source_schema="booking",
        referent_schema="booking",
        onupdate="CASCADE",
        ondelete="SET NULL",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("rooms_main_image_id_fkey", "rooms", schema="booking", type_="foreignkey")
    op.drop_index(
        op.f("ix_booking_rooms_main_image_id"), table_name="rooms", schema="booking"
    )
    op.drop_column("rooms", "main_image_id", schema="booking")
    op.drop_constraint("hotels_main_image_id_fkey", "hotels", schema="booking", type_="foreignkey")
    op.drop_index(
        op.f("ix_booking_hotels_main_image_id"), table_name="hotels", schema="booking"
    )
    op.drop_column("hotels", "main_image_id", schema="booking")
    op.drop_index(
        op.f("ix_booking_images_room_id"), table_name="images", schema="booking"
    )
    op.drop_index(op.f("ix_booking_images_id"), table_name="images", schema="booking")
    op.drop_table("images", schema="booking")
    # ### end Alembic commands ###
