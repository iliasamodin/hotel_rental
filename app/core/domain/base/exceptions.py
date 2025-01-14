class BaseDomainError(Exception):
    """
    Basic exception at domain level.
    """

    def __init__(
        self,
        message: str | None = "Unspecified domain level error.",
        extras: dict | str | Exception | None = None,
        *args,
        **kwargs,
    ):
        self.message = message
        self.extras = extras
