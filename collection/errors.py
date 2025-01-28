from shared.error_helpers.wrapper import ExceptionWrapper


class CreateError(ExceptionWrapper):
    def __init__(self, e: Exception | None = None) -> None:
        super().__init__("create value error", e)


class UpdateError(ExceptionWrapper):
    def __init__(self, e: Exception | None = None) -> None:
        super().__init__("update value error", e)


class SetError(ExceptionWrapper):
    def __init__(self, e: Exception | None = None) -> None:
        super().__init__("set value error", e)


class GetError(ExceptionWrapper):
    def __init__(self, e: Exception | None = None) -> None:
        super().__init__("get value error", e)


class DeleteError(ExceptionWrapper):
    def __init__(self, e: Exception | None = None) -> None:
        super().__init__("delete value error", e)


class KeyNotFoundError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"key {key} not found")


class CreateCollectionError(ExceptionWrapper):
    def __init__(self, e: Exception | None = None) -> None:
        super().__init__("create collection error", e)
