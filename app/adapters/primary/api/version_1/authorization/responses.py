from starlette import status

from app.core.services.authorization.schemas import UserResponseSchema, TokenResponseSchema

from app.adapters.primary.api.base.schemas import BaseErrorResponseSchema
from app.adapters.primary.api.version_1.authorization.docs import RegistrationEnum, AuthenticationEnum


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

authentication_responses = {
    status.HTTP_201_CREATED: {
        "model": TokenResponseSchema,
        "content": {
            "application/json": {
                "examples": {
                    AuthenticationEnum.SUCCESS.name: {
                        "summary": AuthenticationEnum.SUCCESS.name,
                        "value": AuthenticationEnum.SUCCESS.value,
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
                    AuthenticationEnum.NOT_EXISTS_ERR.name: {
                        "summary": AuthenticationEnum.NOT_EXISTS_ERR.name,
                        "value": AuthenticationEnum.NOT_EXISTS_ERR.value,
                    },
                    AuthenticationEnum.INVALID_PASSWORD_ERR.name: {
                        "summary": AuthenticationEnum.INVALID_PASSWORD_ERR.name,
                        "value": AuthenticationEnum.INVALID_PASSWORD_ERR.value,
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
                    AuthenticationEnum.SERVER_ERR.name: {
                        "summary": AuthenticationEnum.SERVER_ERR.name,
                        "value": AuthenticationEnum.SERVER_ERR.value,
                    },
                },
            },
        },
    },
}
