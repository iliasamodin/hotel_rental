from abc import ABC

from app.ports.secondary.db.dao.base import BaseDAOPort


class ResourceManagerDAOPort(BaseDAOPort, ABC):
    """
    Secondary port of DAO for resource manager.
    """
