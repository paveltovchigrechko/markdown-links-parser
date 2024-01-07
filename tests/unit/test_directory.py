"""Unit tests for Directory class"""
from pathlib import Path
import unittest

from app.models.directory import Directory


class TestDirectory(unittest.TestCase):
    def test_init_positive(self):
        current_path = Path(".").resolve()
        current_path_str = str(current_path)
        d = Directory(current_path_str)
        self.assertEqual(d.path, current_path)

    def test_init_negative_path_not_string(self):
        with self.assertRaises(TypeError):
            Directory(0)

    def test_init_negative_not_existent_path(self):
        with self.assertRaises(FileNotFoundError):
            Directory("./non-existent-path")

    def test_init_negative_path_to_file(self):
        with self.assertRaises(ValueError):
            Directory('test_directory.py')

    def test_scan_files_by_extension_positive(self):
        current_file = Path("test_directory.py").resolve()
        d = Directory('.')
        d.scan_files_by_extension(['py'])
        self.assertTrue(d._file_paths)
        self.assertIn(current_file, d._file_paths)

    def test_scan_files_by_extension_pass_not_iterable(self):
        d = Directory('.')
        d.scan_files_by_extension(0)
        self.assertFalse(d._file_paths)

    def test_scan_files_by_extension_pass_invalid_values(self):
        d = Directory('.')
        invalid_values = ['', None, 0, True, ('', 5.6)]
        d.scan_files_by_extension(invalid_values)
        self.assertFalse(d._file_paths)


if __name__ == "__main__":
    unittest.main()
