from app.ports.secondary.db.dao.resource_manager import ResourceManagerDAOPort

from app.adapters.secondary.db.dao.base.dao import BaseDAO


class ResourceManagerDAO(BaseDAO, ResourceManagerDAOPort):
    """
    DAO for resource manager.
    """
