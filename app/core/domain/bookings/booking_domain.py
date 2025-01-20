from datetime import datetime, time, timedelta

from app.settings import settings

from app.core.services.bookings.dtos import RoomDTO, BookingDTO

from app.core.domain.bookings.exceptions import (
    ItemNotExistsError,
    DeletionTimeEndedError,
    ItemNotBelongUserError,
    RentalPeriodError,
    RoomCapacityError,
    RoomAlreadyBookedError,
)

from app.core.services.bookings.schemas import BaseBookingSchema, BookingRequestSchema, RoomSchema


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

        self.check_consistency_of_rental_period()
        self.check_that_rental_period_is_within_upper_limit()
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

    def check_consistency_of_rental_period(self) -> None:
        """
        Check the consistency of the check-in and check-out dates.

        :raise: RentalPeriodError
        """

        if self.booking.check_in_date >= self.booking.check_out_date:
            raise RentalPeriodError(
                message="Check-out date must be later than check-in date.",
                extras={
                    "check_in_date": self.booking.check_in_date.strftime("%Y-%m-%d"),
                    "check_out_date": self.booking.check_out_date.strftime("%Y-%m-%d"),
                },
            )

    def check_that_rental_period_is_within_upper_limit(self) -> None:
        """
        Checking that the rental period
        does not exceed the maximum rental period.

        :raise: RentalPeriodError
        """

        if (self.booking.check_out_date - self.booking.check_in_date).days > settings.MAX_RENTAL_INTERVAL_DAYS:
            raise RentalPeriodError(
                message=f"The maximum rental period is {settings.MAX_RENTAL_INTERVAL_DAYS} days.",
                extras={
                    "check_in_date": self.booking.check_in_date.strftime("%Y-%m-%d"),
                    "check_out_date": self.booking.check_out_date.strftime("%Y-%m-%d"),
                },
            )

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


class DeleteBookingDomainModel:
    def __init__(
        self,
        user_id: int,
        booking_id: int,
        booking: BookingDTO,
    ):
        self.user_id = user_id
        self.booking_id = booking_id
        self.booking = booking

    def execute(self) -> None:
        """
        Preparing a booking for deletion.
        """

        self.check_existence_of_booking()
        self.check_booking_affiliation()
        self.check_availability_for_deletion()

    def check_existence_of_booking(self) -> None:
        """
        Check that the booking with the passed id exists
        in the database.

        :raise: BookingNotExistsError
        """

        if not self.booking:
            raise ItemNotExistsError(
                message="The booking to be deleted is not in the database.",
                extras={
                    "booking_id": self.booking_id,
                },
            )

    def check_booking_affiliation(self) -> None:
        """
        Check that the booking being deleted belongs to the user
        who is deleting it.

        :raise: NotBelongError
        """

        if self.booking.user_id != self.user_id:
            raise ItemNotBelongUserError(
                message="The booking being canceled does not belong to the user who is deleting it.",
                extras={
                    "user_id": self.user_id,
                    "user_id_of_booking": self.booking.user_id,
                },
            )

    def check_availability_for_deletion(self) -> None:
        """
        Check that the time interval
        when booking deletion is available has not yet expired.

        :raise: DeleteTimeError
        """

        latest_cancellation_dt = self.booking.check_in_dt - timedelta(
            hours=settings.BOOKING_CANCELLATION_AVAILABILITY_HOURS,
        )
        if latest_cancellation_dt < settings.CURRENT_DT:
            raise DeletionTimeEndedError(
                message="The time when the booking could be canceled has already expired.",
                extras={
                    "current_dt": settings.CURRENT_DT.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    "latest_cancellation_dt": latest_cancellation_dt.strftime("%Y-%m-%dT%H:%M:%S%z"),
                },
            )
