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