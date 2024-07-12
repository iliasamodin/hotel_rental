from starlette import status

from app.services.bookings.schemas import (
    ServiceVarietyResponseSchema,
    ExtendedHotelResponseSchema,
    PremiumLevelVarietyResponseSchema,
    ExtendedRoomResponseSchema,
    ExtendedBookingResponseSchema,
)

from app.web.api.base.schemas import BaseErrorResponseSchema
from app.web.api.bookings.docs import ServicesEnum, HotelsEnum, PremiumLevelsEnum, RoomsEnum, BookingsEnum


responses_of_services = {
    status.HTTP_200_OK: {
        "model": ServiceVarietyResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    ServicesEnum.SUCCESS.name: {
                        "summary": ServicesEnum.SUCCESS.name,
                        "value": ServicesEnum.SUCCESS.value,
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
                    ServicesEnum.CONSISTENCY_ERR.name: {
                        "summary": ServicesEnum.CONSISTENCY_ERR.name,
                        "value": ServicesEnum.CONSISTENCY_ERR.value,
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
                    ServicesEnum.SERVER_ERR.name: {
                        "summary": ServicesEnum.SERVER_ERR.name,
                        "value": ServicesEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_hotels = {
    status.HTTP_200_OK: {
        "model": ExtendedHotelResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    HotelsEnum.SUCCESS.name: {
                        "summary": HotelsEnum.SUCCESS.name,
                        "value": HotelsEnum.SUCCESS.value,
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
                    HotelsEnum.SERVER_ERR.name: {
                        "summary": HotelsEnum.SERVER_ERR.name,
                        "value": HotelsEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_premium_levels = {
    status.HTTP_200_OK: {
        "model": PremiumLevelVarietyResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    PremiumLevelsEnum.SUCCESS.name: {
                        "summary": PremiumLevelsEnum.SUCCESS.name,
                        "value": PremiumLevelsEnum.SUCCESS.value,
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
                    PremiumLevelsEnum.SERVER_ERR.name: {
                        "summary": PremiumLevelsEnum.SERVER_ERR.name,
                        "value": PremiumLevelsEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_rooms = {
    status.HTTP_200_OK: {
        "model": ExtendedRoomResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    RoomsEnum.SUCCESS.name: {
                        "summary": RoomsEnum.SUCCESS.name,
                        "value": RoomsEnum.SUCCESS.value,
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
                    RoomsEnum.CONSISTENCY_ERR.name: {
                        "summary": RoomsEnum.CONSISTENCY_ERR.name,
                        "value": RoomsEnum.CONSISTENCY_ERR.value,
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
                    RoomsEnum.SERVER_ERR.name: {
                        "summary": RoomsEnum.SERVER_ERR.name,
                        "value": RoomsEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_bookings = {
    status.HTTP_200_OK: {
        "model": ExtendedBookingResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    BookingsEnum.SUCCESS.name: {
                        "summary": BookingsEnum.SUCCESS.name,
                        "value": BookingsEnum.SUCCESS.value,
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
                    BookingsEnum.CONSISTENCY_ERR.name: {
                        "summary": BookingsEnum.CONSISTENCY_ERR.name,
                        "value": BookingsEnum.CONSISTENCY_ERR.value,
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
                    BookingsEnum.SERVER_ERR.name: {
                        "summary": BookingsEnum.SERVER_ERR.name,
                        "value": BookingsEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}
