from sqlalchemy.orm import sessionmaker

from app.dao.bookings.dao import BookingDAO
from app.dao.bookings.schemas import (
    BookingDTO,
    ExtendedBookingDTO,
    RoomDTO,
    ServiceVarietyDTO,
    ExtendedHotelDTO,
    PremiumLevelVarietyDTO,
    ExtendedRoomDTO,
)

from app.domain.bookings.booking_domain import AddBookingDomainModel, DeleteBookingDomainModel
from app.services.bookings.schemas import (
    BaseBookingSchema,
    BookingRequestSchema,
    BookingResponseSchema,
    ExtendedBookingResponseSchema,
    RoomSchema,
    ServiceVarietyResponseSchema,
    ExtendedHotelResponseSchema,
    PremiumLevelVarietyResponseSchema,
    ExtendedRoomResponseSchema,
    HotelSchema,
)
from app.services.check.schemas import HotelsOrRoomsValidator, MinAndMaxDtsValidator, PriceRangeValidator


class BookingService:
    """
    Class of service for booking.
    """

    booking_dao: BookingDAO

    def __init__(self, session_maker: sessionmaker):
        self.session_maker = session_maker

    async def get_services(
        self,
        only_for_hotels_and_only_for_rooms: HotelsOrRoomsValidator,
    ) -> list[ServiceVarietyResponseSchema]:
        """
        Get all service options.

        :return: list of services.
        """

        async with self.session_maker.begin() as session:
            self.booking_dao = BookingDAO(session=session)
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

        async with self.session_maker.begin() as session:
            self.booking_dao = BookingDAO(session=session)
            hotels_dto: list[ExtendedHotelDTO] = await self.booking_dao.get_hotels(
                location=location,
                number_of_guests=number_of_guests,
                stars=stars,
                services=services,
            )

            hotels: list[ExtendedHotelResponseSchema] = []
            for hotel in hotels_dto:
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
                        rooms_quantity=hotel.rooms_quantity,
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

        async with self.session_maker.begin() as session:
            self.booking_dao = BookingDAO(session=session)
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

        async with self.session_maker.begin() as session:
            self.booking_dao = BookingDAO(session=session)
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

        async with self.session_maker.begin() as session:
            self.booking_dao = BookingDAO(session=session)
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

        async with self.session_maker.begin() as session:
            self.booking_dao = BookingDAO(session=session)

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

            booking_dto: BookingDTO = await self.booking_dao.add_booking(
                new_booking=new_booking,
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

        async with self.session_maker.begin() as session:
            self.booking_dao = BookingDAO(session=session)

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
