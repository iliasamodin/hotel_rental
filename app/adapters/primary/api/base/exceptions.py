class BaseApiError(Exception):
    """
    Basic exception at primary adapter level.
    """

    def __init__(
        self,
        message: str | None = "Unspecified primary adapter level error.",
        extras: dict | str | Exception | None = None,
        *args,
        **kwargs,
    ):
        self.message = message
        self.extras = extras
