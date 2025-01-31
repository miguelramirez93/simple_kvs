class ExceptionWrapper(Exception):
    def __init__(self, message: str, e: Exception | None = None) -> None:
        built_message = f"{message}"
        if e is not None:
            built_message = f"{built_message}: {e}"

        super().__init__(built_message)
