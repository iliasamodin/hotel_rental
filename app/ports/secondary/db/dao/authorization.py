from abc import ABC, abstractmethod

from app.ports.secondary.db.dao.base import BaseDAOPort

from app.core.services.authorization.dtos import UserDTO
from app.core.services.authorization.schemas import UserRequestSchema
from app.core.services.check.schemas import UserAuthenticationValidator


class AuthorizationDAOPort(BaseDAOPort, ABC):
    """
    Secondary port of DAO for authorization.
    """

    @abstractmethod
    async def add_user(
        self,
        user: UserRequestSchema,
    ) -> UserDTO: ...

    @abstractmethod
    async def get_user(
        self,
        authentication_data: UserAuthenticationValidator,
    ) -> UserDTO: ...
