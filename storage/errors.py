from shared.error_helpers.wrapper import ExceptionWrapper


class ContainerNotFoundError(ExceptionWrapper):
    def __init__(self, container: str, e: Exception | None = None) -> None:
        super().__init__(f"container {container} not found", e)
