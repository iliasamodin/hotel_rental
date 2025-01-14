class BaseServiceError(Exception):
    """
    Basic exception at service level.
    """

    def __init__(
        self,
        message: str | None = "Unspecified service level error.",
        extras: dict | str | Exception | None = None,
        *args,
        **kwargs,
    ):
        self.message = message
        self.extras = extras
