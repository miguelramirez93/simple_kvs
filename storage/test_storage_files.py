import shutil
from unittest import TestCase
from storage.storage_files import FilesStorage

class TestFilesStorage(TestCase):
    _expected_files_path = "./test_data"
    _expected_container_name = "container_test"

    def test_should_write_data_in_key_file(self):
        file_storage = FilesStorage(self._expected_files_path)
        file_storage.write(self._expected_container_name, "key", '{"foo": "bar"}'.encode())
        try:

            with open(f"{self._expected_files_path}/{self._expected_container_name}/key") as target:
                self.assertEqual(target.read(), '{"foo": "bar"}')
        except FileNotFoundError as e:
            self.fail(f"file was not written as expected: {e}")
        except Exception as e:
            self.fail(f"unexpected exception has occurred: {e}")
        finally:
            shutil.rmtree(f"{self._expected_files_path}")



