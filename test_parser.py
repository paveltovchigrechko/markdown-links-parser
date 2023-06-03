from parser import Link, File, Dir
import unittest


class MarkdownLinkTests(unittest.TestCase):
    def test_init_with_full_link(self):
        link = Link("path/to/file#heading")
        self.assertEqual(link.path, "path/to/")
        self.assertEqual(link.file, "file")
        self.assertEqual(link.heading, "heading")

    def test_init_with_internal_link(self):
        link = Link("#heading")
        self.assertIsNone(link.path)
        self.assertEqual(link.file, "")
        self.assertEqual(link.heading, "heading")

    def test_init_with_external_link(self):
        link = Link("https://example.com/")
        self.assertEqual(link.path, "https://example.com/")
        self.assertEqual(link.file, "")
        self.assertIsNone(link.heading)

    def test_str_with_full_link(self):
        link = Link("path/to/file#heading")
        self.assertEqual(str(link), "path/to/file#heading")

    def test_str_with_internal_link(self):
        link = Link("#heading")
        self.assertEqual(str(link), "#heading")

    def test_str_with_external_link(self):
        link = Link("https://example.com/")
        self.assertEqual(str(link), "https://example.com/")


class FileTests(unittest.TestCase):
    def setUp(self):
        self.path = "path/to/file"
        self.file = File(self.path)

    def test_init(self):
        self.assertEqual(self.file.path, "path/to/")
        self.assertEqual(self.file.name, "file")
        self.assertEqual(self.file.path_with_name, self.path)
        self.assertEqual(self.file.inbound_links, {})
        self.assertEqual(self.file.internal_links, [])
        self.assertEqual(self.file.external_links, [])
        self.assertEqual(self.file.outside_links, [])

    def test_parse_links(self):
        pass

    def test_check_internal_links_positive(self):
        self.file.inbound_links = {"heading1", "heading2", "heading3"}
        self.file.internal_links = [(1, Link("#heading1")),
                                    (10, Link("#heading2")),
                                    (20, Link("#heading3"))]
        broken_links = self.file.check_internal_links()
        self.assertEqual(len(broken_links), 0)

        self.file.internal_links.pop()
        broken_links = self.file.check_internal_links()
        self.assertEqual(len(broken_links), 0)

    def test_check_internal_links_negative(self):
        self.file.inbound_links = {"heading1", "heading2", "heading3"}
        self.file.internal_links = [(1, Link("#heading1")),
                                    (10, Link("#heading2")),
                                    (30, Link("#heading4"))]
        broken_links = self.file.check_internal_links()
        self.assertEqual(len(broken_links), 1)
        self.assertEqual(broken_links[0][0], 30)
        self.assertEqual(broken_links[0][1].heading, "heading4")

        deleted_heading = self.file.inbound_links.pop()
        broken_links = self.file.check_internal_links()
        self.assertEqual(len(broken_links), 2)
        self.assertTrue(broken_links[0][1].heading == deleted_heading or
                        broken_links[1][1].heading == deleted_heading)


class DirTests(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()
