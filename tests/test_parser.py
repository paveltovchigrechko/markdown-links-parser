import unittest

from parser import link, file


class LinkTests(unittest.TestCase):
    def test_init_with_full_link(self):
        test_link = link.Link("path/to/file#heading")
        self.assertEqual(test_link.path, "path/to/")
        self.assertEqual(test_link.file, "file")
        self.assertEqual(test_link.heading, "heading")

    def test_init_with_internal_link(self):
        test_link = link.Link("#heading")
        self.assertIsNone(test_link.path)
        self.assertEqual(test_link.file, "")
        self.assertEqual(test_link.heading, "heading")

    def test_init_with_external_link(self):
        test_link = link.Link("https://example.com/")
        self.assertEqual(test_link.path, "https://example.com/")
        self.assertEqual(test_link.file, "")
        self.assertIsNone(test_link.heading)

    def test_str_with_full_link(self):
        test_link = link.Link("path/to/file#heading")
        self.assertEqual(str(test_link), "path/to/file#heading")

    def test_str_with_internal_link(self):
        test_link = link.Link("#heading")
        self.assertEqual(str(test_link), "#heading")

    def test_str_with_external_link(self):
        test_link = link.Link("https://example.com/")
        self.assertEqual(str(test_link), "https://example.com/")


class FileTests(unittest.TestCase):
    def setUp(self):
        self.path = "path/to/file"
        self.file = file.File(self.path)

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
        self.file.internal_links = [(1, link.Link("#heading1")),
                                    (10, link.Link("#heading2")),
                                    (20, link.Link("#heading3"))]
        broken_links = self.file.check_internal_links()
        self.assertEqual(len(broken_links), 0)

        self.file.internal_links.pop()
        broken_links = self.file.check_internal_links()
        self.assertEqual(len(broken_links), 0)

    def test_check_internal_links_negative(self):
        self.file.inbound_links = {"heading1", "heading2"}
        self.file.internal_links = [(1, link.Link("#heading1")),
                                    (10, link.Link("#heading2")),
                                    (30, link.Link("#heading4"))]
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
