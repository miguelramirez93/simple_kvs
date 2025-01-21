from unittest import TestCase, mock
from storage.storage import Storage
from shared.date.clock import ClockReader
from collection.read_writer import ReadWriter


class TestReadWriter(TestCase):
    _storage_cli: Storage
    _clock_reader: ClockReader

    def setUp(self):
        self._storage_cli = Storage()
        self._clock_reader = ClockReader()

    def test_should_set_new_value(self):
        self._storage_cli.write = mock.MagicMock()
        self._clock_reader.now = mock.MagicMock(return_value="fake-date-time")

        readWriter = ReadWriter(self._storage_cli, self._clock_reader)

        readWriter.set("data", "foo", "bar")

        expectedWrittenBytes = b'{"key": "foo", "value": "bar", "meta": {"created_at": "fake-date-time", "last_update_at": "fake-date-time", "version": 1}}'

        self._storage_cli.write.assert_called_once_with(
            "data", "foo", expectedWrittenBytes)
