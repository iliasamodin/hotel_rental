from app.settings import settings

from app.utils.celery.tasks import send_email

from app.ports.primary.bookings import BookingServicePort
from app.ports.secondary.db.dao.bookings import BookingDAOPort

from app.core.interfaces.transaction_manager import ITransactionManager
from app.core.services.authorization.dtos import UserDTO
from app.core.services.bookings.dtos import (
    BookingDTO,
    ExtendedBookingDTO,
    RoomDTO,
    ServiceVarietyDTO,
    ExtendedHotelDTO,
    PremiumLevelVarietyDTO,
    ExtendedRoomDTO,
)
from app.core.domain.bookings.booking_domain import AddBookingDomainModel, DeleteBookingDomainModel
from app.core.services.bookings.schemas import (
    BaseBookingSchema,
    BookingRequestSchema,
    BookingResponseSchema,
    ExtendedBookingResponseSchema,
    ImageSchema,
    RoomSchema,
    ServiceVarietyResponseSchema,
    ExtendedHotelResponseSchema,
    PremiumLevelVarietyResponseSchema,
    ExtendedRoomResponseSchema,
    HotelSchema,
)
from app.core.services.bookings.templates import (
    body_template_for_booking_confirmation,
    body_template_for_booking_cancellation,
)
from app.core.services.check.schemas import HotelsOrRoomsValidator, MinAndMaxDtsValidator, PriceRangeValidator


class BookingService(BookingServicePort):
    """
    Class of service for booking.
    """

    def __init__(
        self,
        transaction_manager: ITransactionManager,
        booking_dao: BookingDAOPort,
    ):
        self.transaction_manager = transaction_manager
        self.booking_dao = booking_dao

    async def get_services(
        self,
        only_for_hotels_and_only_for_rooms: HotelsOrRoomsValidator,
    ) -> list[ServiceVarietyResponseSchema]:
        """
        Get all service options.

        :return: list of services.
        """

        async with self.transaction_manager(self.booking_dao):
            services_dto: list[ServiceVarietyDTO] = await self.booking_dao.get_services(
                only_for_hotels_and_only_for_rooms=only_for_hotels_and_only_for_rooms,
            )

            services = [
                ServiceVarietyResponseSchema(
                    id=service.id,
                    key=service.key,
                    name=service.name,
                    desc=service.desc,
                )
                for service in services_dto
            ]

        return services

    async def get_hotels(
        self,
        location: str | None = None,
        number_of_guests: int | None = None,
        stars: int | None = None,
        services: list[int] | None = None,
    ) -> list[ExtendedHotelResponseSchema]:
        """
        Get a list of hotels in accordance with filters.

        :return: list of hotels.
        """

        async with self.transaction_manager(self.booking_dao):
            hotels_dto: list[ExtendedHotelDTO] = await self.booking_dao.get_hotels(
                location=location,
                number_of_guests=number_of_guests,
                stars=stars,
                services=services,
            )

            hotels: list[ExtendedHotelResponseSchema] = []
            for hotel in hotels_dto:
                main_image = hotel.main_image and ImageSchema(
                    id=hotel.main_image.id,
                    key=hotel.main_image.key,
                    name=hotel.main_image.name,
                    desc=hotel.main_image.desc,
                    room_id=hotel.main_image.room_id,
                    filepath=hotel.main_image.filepath,
                )

                services = [
                    ServiceVarietyResponseSchema(
                        id=service.id,
                        key=service.key,
                        name=service.name,
                        desc=service.desc,
                    )
                    for service in hotel.services
                ]

                hotels.append(
                    ExtendedHotelResponseSchema(
                        id=hotel.id,
                        name=hotel.name,
                        desc=hotel.desc,
                        location=hotel.location,
                        stars=hotel.stars,
                        main_image_id=hotel.main_image_id,
                        rooms_quantity=hotel.rooms_quantity,
                        main_image=main_image,
                        services=services,
                    )
                )

        return hotels

    async def get_premium_levels(
        self,
        hotel_id: int | None = None,
        connected_with_rooms: bool = False,
    ) -> list[PremiumLevelVarietyResponseSchema]:
        """
        Get all variations of room's premium levels.

        :return: list of premium levels.
        """

        async with self.transaction_manager(self.booking_dao):
            premium_levels_dto: list[PremiumLevelVarietyDTO] = await self.booking_dao.get_premium_levels(
                hotel_id=hotel_id,
                connected_with_rooms=connected_with_rooms,
            )

            premium_levels = [
                PremiumLevelVarietyResponseSchema(
                    id=premium_level.id,
                    key=premium_level.key,
                    name=premium_level.name,
                    desc=premium_level.desc,
                )
                for premium_level in premium_levels_dto
            ]

        return premium_levels

    async def get_rooms(
        self,
        min_price_and_max_price: PriceRangeValidator,
        hotel_id: int = None,
        number_of_guests: int = None,
        services: list[int] | None = None,
        premium_levels: list[int] | None = None,
    ) -> list[ExtendedRoomResponseSchema]:
        """
        Get a list of rooms in accordance with filters.

        :return: list of rooms.
        """

        async with self.transaction_manager(self.booking_dao):
            rooms_dto: list[ExtendedRoomDTO] = await self.booking_dao.get_rooms(
                min_price_and_max_price=min_price_and_max_price,
                hotel_id=hotel_id,
                number_of_guests=number_of_guests,
                services=services,
                premium_levels=premium_levels,
            )

            rooms: list[ExtendedRoomResponseSchema] = []
            for room in rooms_dto:
                hotel = HotelSchema(
                    id=room.hotel.id,
                    name=room.hotel.name,
                    desc=room.hotel.desc,
                    location=room.hotel.location,
                    stars=room.hotel.stars,
                )
                premium_level = room.premium_level and PremiumLevelVarietyResponseSchema(
                    id=room.premium_level.id,
                    key=room.premium_level.key,
                    name=room.premium_level.name,
                    desc=room.premium_level.desc,
                )

                services = [
                    ServiceVarietyResponseSchema(
                        id=service.id,
                        key=service.key,
                        name=service.name,
                        desc=service.desc,
                    )
                    for service in room.services
                ]

                rooms.append(
                    ExtendedRoomResponseSchema(
                        id=room.id,
                        name=room.name,
                        desc=room.desc,
                        hotel_id=room.hotel_id,
                        premium_level_id=room.premium_level_id,
                        ordinal_number=room.ordinal_number,
                        maximum_persons=room.maximum_persons,
                        price=room.price,
                        hotel=hotel,
                        premium_level=premium_level,
                        services=services,
                    )
                )

        return rooms

    async def get_bookings(
        self,
        user_id: int,
        min_and_max_dts: MinAndMaxDtsValidator,
        number_of_guests: int = None,
    ) -> list[ExtendedBookingResponseSchema]:
        """
        Get a list of user's bookings.

        :return: list of bookings.
        """

        async with self.transaction_manager(self.booking_dao):
            bookings_dto: list[ExtendedBookingDTO] = await self.booking_dao.get_bookings(
                user_id=user_id,
                min_and_max_dts=min_and_max_dts,
                number_of_guests=number_of_guests,
            )

            bookings: list[ExtendedBookingResponseSchema] = []
            for booking in bookings_dto:
                bookings.append(
                    ExtendedBookingResponseSchema(
                        id=booking.id,
                        user_id=booking.user_id,
                        room_id=booking.room_id,
                        number_of_persons=booking.number_of_persons,
                        check_in_dt=booking.check_in_dt,
                        check_out_dt=booking.check_out_dt,
                        total_cost=booking.total_cost,
                        room=RoomSchema(
                            id=booking.room.id,
                            name=booking.room.name,
                            desc=booking.room.desc,
                            hotel_id=booking.room.hotel_id,
                            premium_level_id=booking.room.premium_level_id,
                            ordinal_number=booking.room.ordinal_number,
                            maximum_persons=booking.room.maximum_persons,
                            price=booking.room.price,
                        ),
                    )
                )

        return bookings

    async def add_booking(
        self,
        user_id: int,
        booking_data: BookingRequestSchema,
    ) -> BookingResponseSchema:
        """
        Add a booking.

        :return: data of new booking.
        """

        async with self.transaction_manager(self.booking_dao) as session_id:
            room_dto: RoomDTO = await self.booking_dao.get_item_by_id(
                table_name="rooms",
                item_id=booking_data.room_id,
            )

            # Business logic of adding booking
            add_booking_domain_model = AddBookingDomainModel(
                user_id=user_id,
                booking=booking_data,
                room=room_dto,
            )
            new_booking: BaseBookingSchema = add_booking_domain_model.execute()

            min_and_max_dts = MinAndMaxDtsValidator(
                min_dt=new_booking.check_in_dt,
                max_dt=new_booking.check_out_dt,
            )
            overlapping_bookings_dto: list[BookingDTO] = await self.booking_dao.get_bookings(
                min_and_max_dts=min_and_max_dts,
                room_id=new_booking.room_id,
                booking_overlaps=True,
            )
            add_booking_domain_model.check_room_availability(overlapping_bookings=overlapping_bookings_dto)

            booking_dto: BookingDTO = await self.booking_dao.insert_item(
                table_name="bookings",
                item_data=new_booking,
            )

            await self.transaction_manager.commit(session_id=session_id)

            if settings.NEED_TO_SENDING_EMAIL:
                # Generating and sending a message via user email
                user_dto: UserDTO = await self.booking_dao.get_item_by_id(
                    table_name="users",
                    item_id=user_id,
                )
                send_email.delay(
                    receiver_email=user_dto.email,
                    subject="Booking confirmation",
                    body=body_template_for_booking_confirmation.format(
                        room_name=room_dto.name,
                        number_of_persons=booking_dto.number_of_persons,
                        check_in_dt=booking_dto.check_in_dt.strftime("%Y-%m-%d %H:%M"),
                        check_out_dt=booking_dto.check_out_dt.strftime("%Y-%m-%d %H:%M"),
                        total_cost=booking_dto.total_cost,
                    ),
                )

            booking = BookingResponseSchema(
                id=booking_dto.id,
                user_id=booking_dto.user_id,
                room_id=booking_dto.room_id,
                number_of_persons=booking_dto.number_of_persons,
                check_in_dt=booking_dto.check_in_dt,
                check_out_dt=booking_dto.check_out_dt,
                total_cost=booking_dto.total_cost,
            )

        return booking

    async def delete_booking(
        self,
        user_id: int,
        booking_id: int,
    ) -> BookingResponseSchema:
        """
        Delete booking.

        :return: data of deleted booking.
        """

        async with self.transaction_manager(self.booking_dao) as session_id:
            booking_dto: BookingDTO = await self.booking_dao.get_item_by_id(
                table_name="bookings",
                item_id=booking_id,
            )

            # Business logic of deleting booking
            delete_booking_domain_model = DeleteBookingDomainModel(
                user_id=user_id,
                booking_id=booking_id,
                booking=booking_dto,
            )
            delete_booking_domain_model.execute()

            booking_dto: BookingDTO = await self.booking_dao.delete_item_by_id(
                table_name="bookings",
                item_id=booking_id,
            )

            await self.transaction_manager.commit(session_id=session_id)

            if settings.NEED_TO_SENDING_EMAIL:
                # Generating and sending a message via user email
                user_dto: UserDTO = await self.booking_dao.get_item_by_id(
                    table_name="users",
                    item_id=user_id,
                )
                room_dto: RoomDTO = await self.booking_dao.get_item_by_id(
                    table_name="rooms",
                    item_id=booking_dto.room_id,
                )
                send_email.delay(
                    receiver_email=user_dto.email,
                    subject="Booking cancellation",
                    body=body_template_for_booking_cancellation.format(
                        room_name=room_dto.name,
                        number_of_persons=booking_dto.number_of_persons,
                        check_in_dt=booking_dto.check_in_dt.strftime("%Y-%m-%d %H:%M"),
                        check_out_dt=booking_dto.check_out_dt.strftime("%Y-%m-%d %H:%M"),
                        total_cost=booking_dto.total_cost,
                    ),
                )

            booking = BookingResponseSchema(
                id=booking_dto.id,
                user_id=booking_dto.user_id,
                room_id=booking_dto.room_id,
                number_of_persons=booking_dto.number_of_persons,
                check_in_dt=booking_dto.check_in_dt,
                check_out_dt=booking_dto.check_out_dt,
                total_cost=booking_dto.total_cost,
            )

        return booking
