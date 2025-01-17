from shared.error_helpers.wrapper import ExceptionWrapper


class ContainerNotFoundError(ExceptionWrapper):
    def __init__(self, container: str, e: Exception | None = None) -> None:
        super().__init__(f"container {container} not found", e)


class WriteError(ExceptionWrapper):
    def __init__(self, e: Exception | None = None) -> None:
        super().__init__("storage write error", e)

class ReadError(ExceptionWrapper):
    def __init__(self, e: Exception | None = None) -> None:
        super().__init__("storage read error", e)
