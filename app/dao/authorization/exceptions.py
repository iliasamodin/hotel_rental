from app.dao.base.exceptions import BaseDAOError


class BaseAuthorizationDAOError(BaseDAOError):
    """
    Basic exception for authorization DAO.
    """


class DAOConstraintError(BaseAuthorizationDAOError):
    """
    Exception for database constraint violation for DAO authorization.
    """


class NotUniqueError(DAOConstraintError):
    """
    Exception of adding row with non-unique value
    in field that must be unique.
    """


class AlreadyExistsError(NotUniqueError):
    """
    Exception of adding row with a non-unique value
    to the database.
    """
