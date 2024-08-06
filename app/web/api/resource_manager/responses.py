from starlette import status

from app.services.bookings.schemas import (
    ServiceVarietyResponseSchema,
    HotelSchema,
    PremiumLevelVarietyResponseSchema,
    RoomSchema,
)

from app.web.api.base.schemas import BaseErrorResponseSchema
from app.web.api.resource_manager.docs import GettingEntityEnum


responses_of_getting_entity = {
    status.HTTP_200_OK: {
        "model": ServiceVarietyResponseSchema | HotelSchema | PremiumLevelVarietyResponseSchema | RoomSchema,
        "content": {
            "application/json": {
                "examples": {
                    GettingEntityEnum.SUCCESS_FOR_SERVICE.name: {
                        "summary": GettingEntityEnum.SUCCESS_FOR_SERVICE.name,
                        "value": GettingEntityEnum.SUCCESS_FOR_SERVICE.value,
                    },
                    GettingEntityEnum.SUCCESS_FOR_HOTEL.name: {
                        "summary": GettingEntityEnum.SUCCESS_FOR_HOTEL.name,
                        "value": GettingEntityEnum.SUCCESS_FOR_HOTEL.value,
                    },
                    GettingEntityEnum.SUCCESS_FOR_PREMIUM_LEVEL.name: {
                        "summary": GettingEntityEnum.SUCCESS_FOR_PREMIUM_LEVEL.name,
                        "value": GettingEntityEnum.SUCCESS_FOR_PREMIUM_LEVEL.value,
                    },
                    GettingEntityEnum.SUCCESS_FOR_ROOM.name: {
                        "summary": GettingEntityEnum.SUCCESS_FOR_ROOM.name,
                        "value": GettingEntityEnum.SUCCESS_FOR_ROOM.value,
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
                    GettingEntityEnum.SERVER_ERR.name: {
                        "summary": GettingEntityEnum.SERVER_ERR.name,
                        "value": GettingEntityEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}

responses_of_getting_entities = {
    status.HTTP_200_OK: {
        "model": (
            list[ServiceVarietyResponseSchema]
            | list[HotelSchema]
            | list[PremiumLevelVarietyResponseSchema]
            | list[RoomSchema]
        ),
        "content": {
            "application/json": {
                "examples": {
                    GettingEntityEnum.SUCCESS_FOR_SERVICE.name: {
                        "summary": GettingEntityEnum.SUCCESS_FOR_SERVICE.name,
                        "value": [GettingEntityEnum.SUCCESS_FOR_SERVICE.value],
                    },
                    GettingEntityEnum.SUCCESS_FOR_HOTEL.name: {
                        "summary": GettingEntityEnum.SUCCESS_FOR_HOTEL.name,
                        "value": [GettingEntityEnum.SUCCESS_FOR_HOTEL.value],
                    },
                    GettingEntityEnum.SUCCESS_FOR_PREMIUM_LEVEL.name: {
                        "summary": GettingEntityEnum.SUCCESS_FOR_PREMIUM_LEVEL.name,
                        "value": [GettingEntityEnum.SUCCESS_FOR_PREMIUM_LEVEL.value],
                    },
                    GettingEntityEnum.SUCCESS_FOR_ROOM.name: {
                        "summary": GettingEntityEnum.SUCCESS_FOR_ROOM.name,
                        "value": [GettingEntityEnum.SUCCESS_FOR_ROOM.value],
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
                    GettingEntityEnum.SERVER_ERR.name: {
                        "summary": GettingEntityEnum.SERVER_ERR.name,
                        "value": GettingEntityEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}
