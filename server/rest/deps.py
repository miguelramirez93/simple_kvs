from collection.read_writer import ReadWriter
from storage.storage_files import FilesStorage


class Deps():
    collection_read_writer: ReadWriter

    def __init__(self, read_writer_impl: ReadWriter) -> None:
        self.collection_read_writer = read_writer_impl


def init_deps() -> Deps:
    # TODO: Add scope based deps
    # initialization
    storage_impl = FilesStorage()
    deps = Deps(ReadWriter(storage_impl))
    return deps


app_deps = init_deps()
