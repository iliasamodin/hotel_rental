from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import sessionmaker

from app.services.authorization.service import AuthorizationService
from app.services.authorization.schemas import UserRequestSchema, UserResponseSchema
from app.services.check.services import get_session_maker

from app.web.api.authorization.responses import registration_responses

router = APIRouter(prefix="/users")


@router.post(
    path="/registration",
    status_code=201,
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
