from starlette import status

from app.services.authorization.schemas import UserResponseSchema

from app.web.api.base.schemas import BaseErrorResponseSchema
from app.web.api.authorization.docs import RegistrationEnum


registration_responses = {
    status.HTTP_201_CREATED: {
        "model": UserResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    RegistrationEnum.SUCCESS.name: {
                        "summary": RegistrationEnum.SUCCESS.name,
                        "value": RegistrationEnum.SUCCESS.value,
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
                    RegistrationEnum.NOT_UNIQUE_FIELD_ERR.name: {
                        "summary": RegistrationEnum.NOT_UNIQUE_FIELD_ERR.name,
                        "value": RegistrationEnum.NOT_UNIQUE_FIELD_ERR.value,
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
                    RegistrationEnum.DAO_ERR.name: {
                        "summary": RegistrationEnum.DAO_ERR.name,
                        "value": RegistrationEnum.DAO_ERR.value,
                    },
                    RegistrationEnum.SERVER_ERR.name: {
                        "summary": RegistrationEnum.SERVER_ERR.name,
                        "value": RegistrationEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}
