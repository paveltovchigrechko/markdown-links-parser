import parser
import unittest


class MarkdownLinkTests(unittest.TestCase):
    def test_init_with_full_link(self):
        link = parser.MarkdownLink("path/to/file#heading")
        self.assertEqual(link.path, "path/to/")
        self.assertEqual(link.file, "file")
        self.assertEqual(link.heading, "heading")

    def test_init_with_internal_link(self):
        link = parser.MarkdownLink("#heading")
        self.assertIsNone(link.path)
        self.assertEqual(link.file, "")
        self.assertEqual(link.heading, "heading")

    def test_init_with_external_link(self):
        link = parser.MarkdownLink("https://example.com/")
        self.assertEqual(link.path, "https://example.com/")
        self.assertEqual(link.file, "")
        self.assertIsNone(link.heading)

    def test_str_with_full_link(self):
        link = parser.MarkdownLink("path/to/file#heading")
        self.assertEqual(str(link), "path/to/file#heading")

    def test_str_with_internal_link(self):
        link = parser.MarkdownLink("#heading")
        self.assertEqual(str(link), "#heading")

    def test_str_with_external_link(self):
        link = parser.MarkdownLink("https://example.com/")
        self.assertEqual(str(link), "https://example.com/")


class FileTests(unittest.TestCase):
    pass


class DirTests(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
