from starlette import status

from app.services.bookings.schemas import (
    BookingResponseSchema,
    ServiceVarietyResponseSchema,
    ExtendedHotelResponseSchema,
    PremiumLevelVarietyResponseSchema,
    ExtendedRoomResponseSchema,
    ExtendedBookingResponseSchema,
)

from app.web.api.base.schemas import BaseErrorResponseSchema
from app.web.api.bookings.docs import (
    AddingBookingEnum,
    DeletingBookingEnum,
    GettingServicesEnum,
    GettingHotelsEnum,
    GettingPremiumLevelsEnum,
    GettingRoomsEnum,
    GettingBookingsEnum,
)


responses_of_getting_services = {
    status.HTTP_200_OK: {
        "model": ServiceVarietyResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingServicesEnum.SUCCESS.name: {
                        "summary": GettingServicesEnum.SUCCESS.name,
                        "value": GettingServicesEnum.SUCCESS.value,
                    },
                },
            },
        },
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingServicesEnum.CONSISTENCY_ERR.name: {
                        "summary": GettingServicesEnum.CONSISTENCY_ERR.name,
                        "value": GettingServicesEnum.CONSISTENCY_ERR.value,
                    },
                },
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingServicesEnum.SERVER_ERR.name: {
                        "summary": GettingServicesEnum.SERVER_ERR.name,
                        "value": GettingServicesEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_getting_hotels = {
    status.HTTP_200_OK: {
        "model": ExtendedHotelResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingHotelsEnum.SUCCESS.name: {
                        "summary": GettingHotelsEnum.SUCCESS.name,
                        "value": GettingHotelsEnum.SUCCESS.value,
                    },
                },
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingHotelsEnum.SERVER_ERR.name: {
                        "summary": GettingHotelsEnum.SERVER_ERR.name,
                        "value": GettingHotelsEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_getting_premium_levels = {
    status.HTTP_200_OK: {
        "model": PremiumLevelVarietyResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingPremiumLevelsEnum.SUCCESS.name: {
                        "summary": GettingPremiumLevelsEnum.SUCCESS.name,
                        "value": GettingPremiumLevelsEnum.SUCCESS.value,
                    },
                },
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingPremiumLevelsEnum.SERVER_ERR.name: {
                        "summary": GettingPremiumLevelsEnum.SERVER_ERR.name,
                        "value": GettingPremiumLevelsEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_getting_rooms = {
    status.HTTP_200_OK: {
        "model": ExtendedRoomResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingRoomsEnum.SUCCESS.name: {
                        "summary": GettingRoomsEnum.SUCCESS.name,
                        "value": GettingRoomsEnum.SUCCESS.value,
                    },
                },
            },
        },
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingRoomsEnum.CONSISTENCY_ERR.name: {
                        "summary": GettingRoomsEnum.CONSISTENCY_ERR.name,
                        "value": GettingRoomsEnum.CONSISTENCY_ERR.value,
                    },
                },
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingRoomsEnum.SERVER_ERR.name: {
                        "summary": GettingRoomsEnum.SERVER_ERR.name,
                        "value": GettingRoomsEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_getting_bookings = {
    status.HTTP_200_OK: {
        "model": ExtendedBookingResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingBookingsEnum.SUCCESS.name: {
                        "summary": GettingBookingsEnum.SUCCESS.name,
                        "value": GettingBookingsEnum.SUCCESS.value,
                    },
                },
            },
        },
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingBookingsEnum.CONSISTENCY_ERR.name: {
                        "summary": GettingBookingsEnum.CONSISTENCY_ERR.name,
                        "value": GettingBookingsEnum.CONSISTENCY_ERR.value,
                    },
                },
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingBookingsEnum.SERVER_ERR.name: {
                        "summary": GettingBookingsEnum.SERVER_ERR.name,
                        "value": GettingBookingsEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_adding_booking = {
    status.HTTP_201_CREATED: {
        "model": BookingResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    AddingBookingEnum.SUCCESS.name: {
                        "summary": AddingBookingEnum.SUCCESS.name,
                        "value": AddingBookingEnum.SUCCESS.value,
                    },
                },
            },
        },
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    AddingBookingEnum.CONSISTENCY_ERR.name: {
                        "summary": AddingBookingEnum.CONSISTENCY_ERR.name,
                        "value": AddingBookingEnum.CONSISTENCY_ERR.value,
                    },
                },
            },
        },
    },
    status.HTTP_409_CONFLICT: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    AddingBookingEnum.CAPACITY_ERR.name: {
                        "summary": AddingBookingEnum.CAPACITY_ERR.name,
                        "value": AddingBookingEnum.CAPACITY_ERR.value,
                    },
                    AddingBookingEnum.AVAILABILITY_ERR.name: {
                        "summary": AddingBookingEnum.AVAILABILITY_ERR.name,
                        "value": AddingBookingEnum.AVAILABILITY_ERR.value,
                    },
                },
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    AddingBookingEnum.SERVER_ERR.name: {
                        "summary": AddingBookingEnum.SERVER_ERR.name,
                        "value": AddingBookingEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_deleting_booking = {
    status.HTTP_204_NO_CONTENT: {
        "content": {
            "application/json": {
                "examples": {
                    DeletingBookingEnum.SUCCESS.name: {
                        "summary": DeletingBookingEnum.SUCCESS.name,
                        "value": DeletingBookingEnum.SUCCESS.value,
                    },
                },
            },
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    DeletingBookingEnum.NOT_EXISTS_ERR.name: {
                        "summary": DeletingBookingEnum.NOT_EXISTS_ERR.name,
                        "value": DeletingBookingEnum.NOT_EXISTS_ERR.value,
                    },
                },
            },
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    DeletingBookingEnum.CONNECTIVITY_ERR.name: {
                        "summary": DeletingBookingEnum.CONNECTIVITY_ERR.name,
                        "value": DeletingBookingEnum.CONNECTIVITY_ERR.value,
                    },
                },
            },
        },
    },
    status.HTTP_405_METHOD_NOT_ALLOWED: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    DeletingBookingEnum.AVAILABILITY_ERR.name: {
                        "summary": DeletingBookingEnum.AVAILABILITY_ERR.name,
                        "value": DeletingBookingEnum.AVAILABILITY_ERR.value,
                    },
                },
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": BaseErrorResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    DeletingBookingEnum.SERVER_ERR.name: {
                        "summary": DeletingBookingEnum.SERVER_ERR.name,
                        "value": DeletingBookingEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}
