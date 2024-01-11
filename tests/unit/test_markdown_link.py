import unittest

from app.models.markdown_link import MarkdownLink


class LinkTests(unittest.TestCase):
    def test_init_positive_full(self):
        link = MarkdownLink('[link text](path/to/file#heading)')
        self.assertEqual(link.text, 'link text')
        self.assertEqual(link.url_path, 'path/to/')
        self.assertEqual(link.url_file, 'file')
        self.assertEqual(link.url_heading, 'heading')

    def test_init_positive_wo_path(self):
        link = MarkdownLink('[link text](file#heading)')
        self.assertEqual(link.text, 'link text')
        self.assertIsNone(link.url_path)
        self.assertEqual(link.url_file, 'file')
        self.assertEqual(link.url_heading, 'heading')

    def test_init_positive_path_only(self):
        link = MarkdownLink('[link text](some/external/url/)')
        self.assertEqual(link.text, 'link text')
        self.assertEqual(link.url_path, 'some/external/url/')
        self.assertIsNone(link.url_file)
        self.assertIsNone(link.url_heading)

    def test_init_positive_file_only(self):
        link = MarkdownLink('[link text](file)')
        self.assertEqual(link.text, 'link text')
        self.assertIsNone(link.url_path)
        self.assertEqual(link.url_file, 'file')
        self.assertIsNone(link.url_heading)

    def test_init_positive_heading_only(self):
        link = MarkdownLink('[link text](#heading)')
        self.assertEqual(link.text, 'link text')
        self.assertIsNone(link.url_path)
        self.assertIsNone(link.url_file)
        self.assertEqual(link.url_heading, 'heading')

    def test_init_negative_not_str(self):
        with self.assertRaises(TypeError):
            MarkdownLink(0)

    def test_init_negative_empty_str(self):
        with self.assertRaises(ValueError):
            MarkdownLink('')

    def test_str(self):
        link = MarkdownLink('[link text](path/to/file#heading)')
        self.assertEqual(str(link), 'path/to/file#heading')


if __name__ == "__main__":
    unittest.main()