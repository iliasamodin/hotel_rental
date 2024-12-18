from array import array
from collections import defaultdict
from datetime import timedelta

import asyncio

from icecream import ic

from app.main import app  # noqa: F401
from app.settings import settings

from app.redis.redis_controller import redis_controller

from app.celery.celery_controller import celery_controller
from app.celery.templates import body_template_for_booking_reminders
from app.celery.tasks import send_email

from app.dao.base.schemas import OccurrenceFilterDTO
from app.dao.authorization.schemas import UserDTO
from app.dao.bookings.dao import BookingDAO
from app.dao.bookings.schemas import ExtendedBookingDTO

from app.services.check.schemas import MinAndMaxDtsValidator


@celery_controller.task(name="booking_reminders")
def booking_reminders(
    body_template: str = body_template_for_booking_reminders,
) -> None:
    """
    Send booking reminders.

    :return: message sending status.
    """

    with celery_controller.session_maker.begin() as session:
        booking_dao = BookingDAO(session=session)

        dts_of_soon_bookings = MinAndMaxDtsValidator(
            min_dt=settings.CURRENT_DT,
            max_dt=settings.CURRENT_DT + timedelta(hours=settings.NOTIFICATION_ABOUT_SOON_BOOKING_HOURS),
        )
        bookings: list[ExtendedBookingDTO] = asyncio.run(
            booking_dao.get_bookings(min_and_max_dts=dts_of_soon_bookings),
        )

        map_of_user_ids_and_soon_bookings: dict[int, list[ExtendedBookingDTO]] = defaultdict(list)
        for booking in bookings:
            map_of_user_ids_and_soon_bookings[booking.user_id].append(booking)

        try:
            occurrence_filter = OccurrenceFilterDTO[int](
                column_name="id",
                array=array("i", map_of_user_ids_and_soon_bookings.keys()),
            )

        except ValueError:
            ic("There are no soon user bookings.")
            return False

        users: list[UserDTO] = asyncio.run(
            booking_dao.get_items_by_filters(
                table_name="users",
                occurrence=occurrence_filter,
            ),
        )

    for user in users:
        soon_bookings_of_user = map_of_user_ids_and_soon_bookings[user.id]
        for booking in soon_bookings_of_user:
            send_email.delay(
                receiver_email=user.email,
                subject="We remind you about booking",
                body=body_template.format(
                    room_name=booking.room.name,
                    number_of_persons=booking.number_of_persons,
                    check_in_dt=booking.check_in_dt.strftime("%Y-%m-%d %H:%M"),
                    check_out_dt=booking.check_out_dt.strftime("%Y-%m-%d %H:%M"),
                    total_cost=booking.total_cost,
                ),
            )

    return True


@celery_controller.task(name="warm_up_cache")
def warm_up_cache():
    """
    Warm up redis cache.

    :return: cache warm-up status.
    """

    warm_up_status: bool = redis_controller.warm_up_cache()

    return warm_up_status
