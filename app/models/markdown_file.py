"""
Everything related to MarkdownFile class.
"""
from pathlib import Path
import re

from app.models.markdown_link import MarkdownLink
from app.utils import constants, utils


class MarkdownFile:
    """
    Class for a Markdown file (.md and .mdx extrensions).
    """

    def __init__(self, path: Path) -> None:
        if not isinstance(path, Path):
            raise TypeError('File path must be of pathlib.Path type.')

        if path.exists():
            self._path = path.resolve()
        else:
            raise ValueError(f'File "{str(path)}" does not exist.')

        self._headings = set()
        self._markdown_links = []

    @property
    def path(self):
        return self._path

    @property
    def path_wo_name(self):
        return re.match(constants.SPLIT_LINK_PATTERN, str(self.path)).group(1)

    @property
    def name(self):
        return re.match(constants.SPLIT_LINK_PATTERN, str(self.path)).group(2)

    @property
    def headings(self):
        return self._headings

    @property
    def markdown_links(self):
        return self._markdown_links

    @property
    def outbound_links(self):
        for line_num, markdown_link in self.markdown_links:
            if markdown_link.type.value == 'outbound':
                yield line_num, markdown_link

    def parse_links_and_headings(self,
                                 ignore_commented_lines: bool = True,
                                 commented_pattern: re.Pattern[str] = None) -> None:
        if not self.path.exists():
            raise FileNotFoundError(f'File {self.path} was not found.')
        with open(self.path) as file:
            for (line_num, line) in enumerate(file, start=1):
                # Skip commented line
                if ignore_commented_lines and utils.is_commented_line(commented_pattern, line):
                    continue

                # Check if the line is a heading
                parse_heading_result = utils.parse_heading(line)
                for result in parse_heading_result:
                    if result:
                        self._headings.add(result)

                # Check if the line contains Markdown links
                markdown_links_list = re.findall(constants.MARKDOWN_FULL_LINK_PATTERN, line)
                for link in markdown_links_list:
                    try:
                        m = MarkdownLink(str(link))
                    except ValueError:
                        continue
                    else:
                        self._markdown_links.append((line_num, m))

    def check_inbound_links(self):
        broken_links = []
        for line_num, link in self._markdown_links:
            if link.type.value == 'inbound':
                if link.url_heading not in self._headings:
                    broken_links.append((line_num, link))
            else:
                pass
        return broken_links

    def search(self, string_to_search, case_sensitive: bool = True) -> list[tuple[int, int]]:
        if not self.path.exists():
            raise FileNotFoundError(f'File {self.path} was not found.')
        if case_sensitive:
            string_to_search = string_to_search.lower()

        search_matches = []

        with open(self.path) as file:
            for (line_num, line) in enumerate(file, start=1):
                lower_line = line.lower()
                occurrences = re.findall(string_to_search, lower_line)
                if occurrences:
                    search_matches.append((line_num, len(occurrences)))
        return search_matches


if __name__ == "__main__":
    pass
