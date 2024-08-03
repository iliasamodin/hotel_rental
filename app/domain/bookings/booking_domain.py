from datetime import datetime, time, timezone

from app.settings import settings

from app.dao.bookings.schemas import RoomDTO, BookingDTO

from app.domain.bookings.exceptions import RoomCapacityError

from app.services.bookings.exceptions import RoomAlreadyBookedError
from app.services.bookings.schemas import BaseBookingSchema, BookingRequestSchema, RoomSchema


class AddBookingDomainModel:
    def __init__(
        self,
        user_id: int,
        booking: BookingRequestSchema | BookingDTO,
        room: RoomSchema | RoomDTO,
    ):
        self.user_id = user_id
        self.booking = booking
        self.room = room

    def execute(self) -> BaseBookingSchema:
        """
        Calculate dates and cost of booking a room.

        :return: data for new booking.
        """

        self.check_number_of_persons()


        check_in_time = time(
            hour=settings.CHECK_IN_TIME,
            tzinfo=settings.DB_TIME_ZONE,
        )
        check_in_dt = datetime.combine(
            date=self.booking.check_in_date,
            time=check_in_time,
        )
        check_out_time = time(
            hour=settings.CHECK_OUT_TIME,
            tzinfo=settings.DB_TIME_ZONE,
        )
        check_out_dt = datetime.combine(
            date=self.booking.check_out_date,
            time=check_out_time,
        )

        number_of_rental_days = (self.booking.check_out_date - self.booking.check_in_date).days
        total_cost = self.room.price * number_of_rental_days

        booking = BaseBookingSchema(
            user_id=self.user_id,
            room_id=self.room.id,
            number_of_persons=self.booking.number_of_persons,
            check_in_dt=check_in_dt,
            check_out_dt=check_out_dt,
            total_cost=total_cost,
        )

        return booking

    def check_number_of_persons(self) -> None:
        """
        Checking that the number of people booking a room
        does not exceed the room's capacity.

        :raise: RoomCapacityError
        """

        if self.booking.number_of_persons < 1:
            raise RoomCapacityError(
                message="The number of person booked must be a positive number.",
                extras={
                    "number_of_person_booked": self.booking.number_of_persons,
                },
            )

        elif self.booking.number_of_persons > self.room.maximum_persons:
            raise RoomCapacityError(
                message="The room capacity is less than the number of person booked.",
                extras={
                    "room_id": self.room.id,
                    "room_name": self.room.name,
                    "maximum_persons_of_room": self.room.maximum_persons,
                    "number_of_person_booked": self.booking.number_of_persons,
                },
            )

    def check_room_availability(
        self,
        overlapping_bookings: list[BookingRequestSchema] | list[BookingDTO],
    ) -> None:
        """
        Checking that the room is not already booked on these dates.

        :raise: RoomAlreadyBookedError
        """

        if overlapping_bookings:
            overlapping_dates = [
                {
                    "check_in_date": booking.check_in_dt.strftime("%Y-%m-%d"),
                    "check_out_date": booking.check_out_dt.strftime("%Y-%m-%d"),
                }
                for booking in overlapping_bookings
            ]
            overlapping_dates.sort(key=lambda dts_of_booking: dts_of_booking["check_in_date"])

            raise RoomAlreadyBookedError(
                    message="The room is already booked on these dates.",
                    extras=overlapping_dates,
                )
