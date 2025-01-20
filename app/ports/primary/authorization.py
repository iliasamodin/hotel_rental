from abc import ABC, abstractmethod

from app.core.services.authorization.schemas import TokenResponseSchema, UserRequestSchema, UserResponseSchema
from app.core.services.check.schemas import UserAuthenticationValidator


class AuthorizationServicePort(ABC):
    """
    Primary port of service for authorization.
    """

    @abstractmethod
    async def registration(
        self,
        user: UserRequestSchema,
    ) -> UserResponseSchema: ...

    @abstractmethod
    async def authentication(
        self,
        authentication_data: UserAuthenticationValidator,
    ) -> TokenResponseSchema: ...
