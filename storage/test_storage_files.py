from unittest import TestCase, mock

from storage.errors import DataNotFoundError, DeleteError, ReadError, WriteError
from storage.storage_files import FilesStorage


class TestFilesStorage(TestCase):
    _expected_files_path = "./test_data"
    _expected_container_name = "container_test"
    _expected_file_content = '{"foo": "bar"}'.encode()

    def setUp(self):
        self.file_storage = FilesStorage(self._expected_files_path)

    def test_should_write_data_in_key_ref_file(self):
        m = mock.mock_open()
        with mock.patch("builtins.open", m, create=True):
            self.file_storage.write(
                self._expected_container_name, "key", self._expected_file_content)

            m.assert_called_once_with(
                f"{self._expected_files_path}/{self._expected_container_name}/key", "w+b")
            handle = m()
            handle.write.assert_called_once_with(self._expected_file_content)

    def test_should_rise_write_error(self):
        m = mock.mock_open()
        with mock.patch("builtins.open", m, create=True) as mocked_open:
            mocked_open.side_effect = IOError()
            with self.assertRaises(WriteError):
                self.file_storage.write(
                    self._expected_container_name, "key", self._expected_file_content)

    def test_should_read_key_file_content(self):
        m = mock.mock_open(read_data=self._expected_file_content)
        with mock.patch("builtins.open", m, create=True):
            value = self.file_storage.get(self._expected_container_name, "key")
            self.assertEqual(value, self._expected_file_content)

            m.assert_called_once_with(
                f"{self._expected_files_path}/{self._expected_container_name}/key", "rb")

            handle = m()
            handle.read.assert_called_once_with()

    def test_should_rise_read_error(self):
        m = mock.mock_open()
        with mock.patch("builtins.open", m, create=True) as mocked_open:
            mocked_open.side_effect = IOError()
            with self.assertRaises(ReadError):
                self.file_storage.get(self._expected_container_name, "key")

    @mock.patch("os.remove")
    def test_should_delete_key_ref_file(self, mock_remove):
        self.file_storage.delete(
            self._expected_container_name, "key")

        mock_remove.assert_called_once_with(
            f"{self._expected_files_path}/{self._expected_container_name}/key")

    @mock.patch("os.remove")
    def test_should_raise_delete_error(self, mock_remove):
        mock_remove.side_effect = IOError()

        with self.assertRaises(DeleteError):
            self.file_storage.delete(
                self._expected_container_name, "key")
            mock_remove.assert_called_once_with(
                f"{self._expected_files_path}/{self._expected_container_name}/key")

    @mock.patch("os.remove")
    def test_should_raise_DataNotFound_delete_error_when_key_file_not_found(self, mock_remove):
        mock_remove.side_effect = FileNotFoundError()

        with self.assertRaises(DataNotFoundError):
            self.file_storage.delete(
                self._expected_container_name, "key")
            mock_remove.assert_called_once_with(
                f"{self._expected_files_path}/{self._expected_container_name}/key")
