from fastapi import Depends, Response
from fastapi.routing import APIRouter
from sqlalchemy.orm import sessionmaker
from starlette import status

from app.settings import settings

from app.services.authorization.service import AuthorizationService
from app.services.authorization.schemas import UserRequestSchema, UserResponseSchema, TokenResponseSchema
from app.services.check.services import get_session_maker
from app.services.check.schemas import UserAuthenticationValidator

from app.web.api.authorization.responses import registration_responses, authentication_responses

router = APIRouter(prefix="/users")


@router.post(
    path="/registration",
    status_code=status.HTTP_201_CREATED,
    responses=registration_responses,
    summary="User registration.",
)
async def registration(
    user: UserRequestSchema,
    session_maker: sessionmaker = Depends(get_session_maker),
) -> UserResponseSchema:
    authorization_service = AuthorizationService(session_maker=session_maker)
    user = await authorization_service.registration(user=user)

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
    session_maker: sessionmaker = Depends(get_session_maker),
) -> TokenResponseSchema:
    authorization_service = AuthorizationService(session_maker=session_maker)
    access_token = await authorization_service.authentication(authentication_data=authentication_data)

    response.set_cookie(
        key=settings.ACCESS_TOKEN_COOKIE,
        value=access_token.token,
        expires=access_token.expires,
    )

    return access_token
