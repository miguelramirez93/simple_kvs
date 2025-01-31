import datetime
from typing import override
from unittest import TestCase, mock

from collection.errors import GetError, KeyNotFoundError, SetError
from collection.item import Item, Metadata
from collection.read_writer import ReadWriter
from shared.date.clock import ClockReader
from storage.errors import DataNotFoundError
from storage.storage import Storage


class TestReadWriter(TestCase):
    _storage_cli: Storage
    _clock_reader: ClockReader

    _expected_date_time: datetime.datetime = datetime.datetime(2020, 5, 17)
    _expected_date_time_str: str = _expected_date_time.strftime(
        "%m/%d/%Y, %H:%M:%S")
    _expected_read_item: Item = Item("foo", "bar", Metadata(
        _expected_date_time_str, _expected_date_time_str, 1))

    _expected_key_value_bytes: bytes = b'{"key": "foo", "value": "bar", "meta": {"created_at": "05/17/2020, 00:00:00", "last_update_at": "05/17/2020, 00:00:00", "version": 1}}'

    @override
    def setUp(self):
        self._storage_cli = mock.ANY
        self._clock_reader = mock.ANY

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
            _ = read_writer.get("data", "foo")
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
        self._clock_reader.now = mock.MagicMock(
            return_value=self._expected_date_time)

        read_writer = ReadWriter(self._storage_cli, self._clock_reader)

        read_writer.set("data", "foo", "bar")

        self._storage_cli.get.assert_called_once_with("data", "foo")
        self._storage_cli.write.assert_called_once_with(
            "data", "foo", self._expected_key_value_bytes)

    def test_should_set_existent_value_if_key_found_in_storage(self):
        self._storage_cli.get = mock.MagicMock(
            return_value=self._expected_key_value_bytes)
        self._storage_cli.write = mock.MagicMock()
        self._clock_reader.now = mock.MagicMock(
            return_value=datetime.datetime(2020, 6, 17))

        read_writer = ReadWriter(self._storage_cli, self._clock_reader)

        read_writer.set("data", "foo", "doe")

        expectedWrittenBytes = b'{"key": "foo", "value": "doe", "meta": {"created_at": "05/17/2020, 00:00:00", "last_update_at": "06/17/2020, 00:00:00", "version": 2}}'

        self._storage_cli.get.assert_called_once_with("data", "foo")
        self._storage_cli.write.assert_called_once_with(
            "data", "foo", expectedWrittenBytes)

    def test_should_raise_set_error_setting_data_in_storage_failure(self):
        self._storage_cli.get = mock.MagicMock(
            return_value=self._expected_key_value_bytes)
        self._storage_cli.write = mock.MagicMock()
        self._storage_cli.write.side_effect = Exception("fake")
        self._clock_reader.now = mock.MagicMock(
            return_value=datetime.datetime(2020, 6, 17))

        read_writer = ReadWriter(self._storage_cli, self._clock_reader)

        with self.assertRaises(SetError):
            read_writer.set("data", "foo", "doe")

        expectedWrittenBytes = b'{"key": "foo", "value": "doe", "meta": {"created_at": "05/17/2020, 00:00:00", "last_update_at": "06/17/2020, 00:00:00", "version": 2}}'
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
