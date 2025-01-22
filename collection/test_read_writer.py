from unittest import TestCase, mock
from storage.storage import Storage
from shared.date.clock import ClockReader
from collection.read_writer import ReadWriter
from collection.item import Item, Metadata
from collection.errors import GetError


class TestReadWriter(TestCase):
    _storage_cli: Storage
    _clock_reader: ClockReader

    _expected_read_item = Item("foo", "bar", Metadata(
        "fake-date-time", "fake-date-time", 1))
    _expected_key_value_bytes = b'{"key": "foo", "value": "bar", "meta": {"created_at": "fake-date-time", "last_update_at": "fake-date-time", "version": 1}}'

    def setUp(self):
        self._storage_cli = Storage()
        self._clock_reader = ClockReader()

    def test_should_get_data(self):
        self._storage_cli.get = mock.MagicMock(
            return_value=self._expected_key_value_bytes)

        read_writer = ReadWriter(self._storage_cli)

        item_found = read_writer.get("data", "foo")

        self.assertEqual(self._expected_read_item, item_found)
        self._storage_cli.get.assert_called_once_with("data", "foo")

    def test_should_rise_get_error_getting_data_from_storage(self):
        self._storage_cli.get = mock.MagicMock()
        self._storage_cli.get.side_effect = Exception("fake")

        read_writer = ReadWriter(self._storage_cli)

        with self.assertRaises(GetError):
            item_found = read_writer.get("data", "foo")

    def test_should_set_new_value(self):
        self._storage_cli.write = mock.MagicMock()
        self._clock_reader.now = mock.MagicMock(return_value="fake-date-time")

        read_writer = ReadWriter(self._storage_cli, self._clock_reader)

        read_writer.set("data", "foo", "bar")

        expectedWrittenBytes = b'{"key": "foo", "value": "bar", "meta": {"created_at": "fake-date-time", "last_update_at": "fake-date-time", "version": 1}}'

        self._storage_cli.write.assert_called_once_with(
            "data", "foo", expectedWrittenBytes)
