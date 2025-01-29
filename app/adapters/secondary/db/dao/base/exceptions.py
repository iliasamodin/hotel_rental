class BaseDAOError(Exception):
    """
    Basic exception at database level.
    """

    def __init__(
        self,
        message: str | None = "Unspecified DAO level error.",
        extras: dict | str | Exception | None = None,
        *args,
        **kwargs,
    ):
        self.message = message
        self.extras = extras


class ModelNotFoundError(BaseDAOError):
    """
    Model not found error.
    """


class ValidatorGenerationError(BaseDAOError):
    """
    Validator generation error.
    """


class TransactionContextAttrNotSetError(BaseDAOError):
    """
    Transaction context attribute not set.
    """


class TransactionContextAttrAlreadySetError(BaseDAOError):
    """
    Transaction context attribute already set.
    """
