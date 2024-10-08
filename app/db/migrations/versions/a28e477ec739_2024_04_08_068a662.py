"""2024-04-08_068a662

Revision ID: a28e477ec739
Revises: 
Create Date: 2024-04-08 12:41:59.527700

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a28e477ec739"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column("stars", sa.Integer(), nullable=True),
        sa.Column("rooms_quantity", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_hotels_id"), "hotels", ["id"], unique=True, schema="booking"
    )
    op.create_index(
        op.f("ix_booking_hotels_location"),
        "hotels",
        ["location"],
        unique=False,
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_hotels_stars"),
        "hotels",
        ["stars"],
        unique=False,
        schema="booking",
    )
    op.create_table(
        "premium_level_varieties",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("desc", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_premium_level_varieties_id"),
        "premium_level_varieties",
        ["id"],
        unique=True,
        schema="booking",
    )
    op.create_table(
        "service_varieties",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("desc", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_service_varieties_id"),
        "service_varieties",
        ["id"],
        unique=True,
        schema="booking",
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_users_email"),
        "users",
        ["email"],
        unique=True,
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_users_id"), "users", ["id"], unique=True, schema="booking"
    )
    op.create_index(
        op.f("ix_booking_users_last_name"),
        "users",
        ["last_name"],
        unique=False,
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_users_phone"),
        "users",
        ["phone"],
        unique=True,
        schema="booking",
    )
    op.create_table(
        "hotels_services",
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("service_variety_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"], ["booking.hotels.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["service_variety_id"],
            ["booking.service_varieties.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("hotel_id", "service_variety_id"),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_hotels_services_hotel_id"),
        "hotels_services",
        ["hotel_id"],
        unique=False,
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_hotels_services_service_variety_id"),
        "hotels_services",
        ["service_variety_id"],
        unique=False,
        schema="booking",
    )
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("premium_level_id", sa.Integer(), nullable=True),
        sa.Column("ordinal_number", sa.Integer(), nullable=False),
        sa.Column("maximum_persons", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"], ["booking.hotels.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["premium_level_id"],
            ["booking.premium_level_varieties.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_rooms_hotel_id"),
        "rooms",
        ["hotel_id"],
        unique=False,
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_rooms_id"), "rooms", ["id"], unique=True, schema="booking"
    )
    op.create_index(
        op.f("ix_booking_rooms_premium_level_id"),
        "rooms",
        ["premium_level_id"],
        unique=False,
        schema="booking",
    )
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("room_id", sa.Integer(), nullable=True),
        sa.Column("number_of_persons", sa.Integer(), nullable=False),
        sa.Column("check_in_dt", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("check_out_dt", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("total_cost", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"], ["booking.rooms.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["booking.users.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_bookings_id"),
        "bookings",
        ["id"],
        unique=True,
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_bookings_room_id"),
        "bookings",
        ["room_id"],
        unique=False,
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_bookings_user_id"),
        "bookings",
        ["user_id"],
        unique=False,
        schema="booking",
    )
    op.create_table(
        "rooms_services",
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("service_variety_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"], ["booking.rooms.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["service_variety_id"],
            ["booking.service_varieties.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("room_id", "service_variety_id"),
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_rooms_services_room_id"),
        "rooms_services",
        ["room_id"],
        unique=False,
        schema="booking",
    )
    op.create_index(
        op.f("ix_booking_rooms_services_service_variety_id"),
        "rooms_services",
        ["service_variety_id"],
        unique=False,
        schema="booking",
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_booking_rooms_services_service_variety_id"),
        table_name="rooms_services",
        schema="booking",
    )
    op.drop_index(
        op.f("ix_booking_rooms_services_room_id"),
        table_name="rooms_services",
        schema="booking",
    )
    op.drop_table("rooms_services", schema="booking")
    op.drop_index(
        op.f("ix_booking_bookings_user_id"), table_name="bookings", schema="booking"
    )
    op.drop_index(
        op.f("ix_booking_bookings_room_id"), table_name="bookings", schema="booking"
    )
    op.drop_index(
        op.f("ix_booking_bookings_id"), table_name="bookings", schema="booking"
    )
    op.drop_table("bookings", schema="booking")
    op.drop_index(
        op.f("ix_booking_rooms_premium_level_id"), table_name="rooms", schema="booking"
    )
    op.drop_index(op.f("ix_booking_rooms_id"), table_name="rooms", schema="booking")
    op.drop_index(
        op.f("ix_booking_rooms_hotel_id"), table_name="rooms", schema="booking"
    )
    op.drop_table("rooms", schema="booking")
    op.drop_index(
        op.f("ix_booking_hotels_services_service_variety_id"),
        table_name="hotels_services",
        schema="booking",
    )
    op.drop_index(
        op.f("ix_booking_hotels_services_hotel_id"),
        table_name="hotels_services",
        schema="booking",
    )
    op.drop_table("hotels_services", schema="booking")
    op.drop_index(op.f("ix_booking_users_phone"), table_name="users", schema="booking")
    op.drop_index(
        op.f("ix_booking_users_last_name"), table_name="users", schema="booking"
    )
    op.drop_index(op.f("ix_booking_users_id"), table_name="users", schema="booking")
    op.drop_index(op.f("ix_booking_users_email"), table_name="users", schema="booking")
    op.drop_table("users", schema="booking")
    op.drop_index(
        op.f("ix_booking_service_varieties_id"),
        table_name="service_varieties",
        schema="booking",
    )
    op.drop_table("service_varieties", schema="booking")
    op.drop_index(
        op.f("ix_booking_premium_level_varieties_id"),
        table_name="premium_level_varieties",
        schema="booking",
    )
    op.drop_table("premium_level_varieties", schema="booking")
    op.drop_index(
        op.f("ix_booking_hotels_stars"), table_name="hotels", schema="booking"
    )
    op.drop_index(
        op.f("ix_booking_hotels_location"), table_name="hotels", schema="booking"
    )
    op.drop_index(op.f("ix_booking_hotels_id"), table_name="hotels", schema="booking")
    op.drop_table("hotels", schema="booking")
    # ### end Alembic commands ###
