class BaseServiceError(Exception):
    """
    Basic exception at service level.
    """

    def __init__(
        self, 
        message: str = None, 
        extras: dict | str | Exception = None, 
        *args,
        **kwargs,
    ):
        self.message = message
        self.extras = extras
