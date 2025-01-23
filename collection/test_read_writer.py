from unittest import TestCase, mock
from storage.storage import Storage
from storage.errors import DataNotFoundError
from shared.date.clock import ClockReader
from collection.read_writer import ReadWriter
from collection.item import Item, Metadata
from collection.errors import GetError, SetError, KeyNotFoundError


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

    def test_should_rise_get_error_getting_data_from_storage_failed(self):
        self._storage_cli.get = mock.MagicMock()
        self._storage_cli.get.side_effect = Exception("fake")
        read_writer = ReadWriter(self._storage_cli)

        with self.assertRaises(GetError):
            item_found = read_writer.get("data", "foo")
            self._storage_cli.get.assert_called_once_with("data", "foo")

    def test_should_return_none_if_no_such_key_in_storage(self):
        self._storage_cli.get = mock.MagicMock()
        self._storage_cli.get.side_effect = DataNotFoundError()

        read_writer = ReadWriter(self._storage_cli)

        item_found = read_writer.get("data", "foo")

        self.assertIsNone(item_found)

        self._storage_cli.get.assert_called_once_with("data", "foo")

    def test_should_set_new_value_if_key_not_found_in_storage(self):
        self._storage_cli.get = mock.MagicMock()
        self._storage_cli.get.side_effect = DataNotFoundError()
        self._storage_cli.write = mock.MagicMock()
        self._clock_reader.now = mock.MagicMock(return_value="fake-date-time")

        read_writer = ReadWriter(self._storage_cli, self._clock_reader)

        read_writer.set("data", "foo", "bar")

        expectedWrittenBytes = b'{"key": "foo", "value": "bar", "meta": {"created_at": "fake-date-time", "last_update_at": "fake-date-time", "version": 1}}'

        self._storage_cli.get.assert_called_once_with("data", "foo")
        self._storage_cli.write.assert_called_once_with(
            "data", "foo", expectedWrittenBytes)

    def test_should_set_existent_value_if_key_found_in_storage(self):
        self._storage_cli.get = mock.MagicMock(
            return_value=self._expected_key_value_bytes)
        self._storage_cli.write = mock.MagicMock()
        self._clock_reader.now = mock.MagicMock(
            return_value="fake-date-time-2")

        read_writer = ReadWriter(self._storage_cli, self._clock_reader)

        read_writer.set("data", "foo", "doe")

        expectedWrittenBytes = b'{"key": "foo", "value": "doe", "meta": {"created_at": "fake-date-time-2", "last_update_at": "fake-date-time-2", "version": 2}}'

        self._storage_cli.get.assert_called_once_with("data", "foo")
        self._storage_cli.write.assert_called_once_with(
            "data", "foo", expectedWrittenBytes)

    def test_should_raise_set_error_setting_data_in_storage_failure(self):
        self._storage_cli.get = mock.MagicMock(
            return_value=self._expected_key_value_bytes)
        self._storage_cli.write = mock.MagicMock()
        self._storage_cli.write.side_effect = Exception("fake")
        self._clock_reader.now = mock.MagicMock(
            return_value="fake-date-time-2")

        read_writer = ReadWriter(self._storage_cli, self._clock_reader)

        with self.assertRaises(SetError):
            read_writer.set("data", "foo", "doe")
            self._storage_cli.get.assert_called_once_with("data", "foo")
            self._storage_cli.write.assert_called_once_with(
                "data", "foo", expectedWrittenBytes)

    def test_should_delete_key_value(self):
        self._storage_cli.delete = mock.MagicMock()

        read_writer = ReadWriter(self._storage_cli, self._clock_reader)

        read_writer.delete("data", "foo")

        self._storage_cli.delete.assert_called_once_with("data", "foo")

    def test_should_raise_key_not_found_error_delete_nonexistent_key_value(self):
        self._storage_cli.delete = mock.MagicMock()
        self._storage_cli.delete.side_effect = DataNotFoundError()

        read_writer = ReadWriter(self._storage_cli, self._clock_reader)

        with self.assertRaises(KeyNotFoundError):
            read_writer.delete("data", "foo")
            self._storage_cli.delete.assert_called_once_with("data", "foo")
