from fastapi import Depends, Response
from fastapi.routing import APIRouter
from starlette import status

from app.settings import settings

from app.ports.primary.authorization import AuthorizationServicePort

from app.core.services.authorization.schemas import UserRequestSchema, UserResponseSchema, TokenResponseSchema
from app.core.services.check.schemas import UserAuthenticationValidator

from app.adapters.primary.api.version_1.authorization.responses import registration_responses, authentication_responses

from app.dependencies.authorization import get_authorization_service

router = APIRouter(prefix="/users")


@router.post(
    path="/registration",
    status_code=status.HTTP_201_CREATED,
    responses=registration_responses,
    summary="User registration.",
)
async def registration(
    user: UserRequestSchema,
    service: AuthorizationServicePort = Depends(get_authorization_service),
) -> UserResponseSchema:
    user = await service.registration(user=user)

    return user


@router.post(
    path="/authentication",
    status_code=status.HTTP_201_CREATED,
    responses=authentication_responses,
    summary="User authentication.",
)
async def authentication(
    response: Response,
    authentication_data: UserAuthenticationValidator,
    service: AuthorizationServicePort = Depends(get_authorization_service),
) -> TokenResponseSchema:
    access_token = await service.authentication(authentication_data=authentication_data)

    response.set_cookie(
        key=settings.ACCESS_TOKEN_COOKIE,
        value=access_token.token,
        expires=access_token.expires,
    )

    return access_token
