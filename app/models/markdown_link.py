"""
Everything related to MarkdownLink class.
"""
from enum import Enum
import re

import app.utils.constants as constants


class MarkdownLink:
    """
    Class for a Markdown link. A link generally has `[some text](path/to/file#heading)` format where
    `some text` is a link text, `path/to` is a path, `file` is a file, and `heading` is a heading.
    """

    def __init__(self, full_link_string: str) -> None:
        """

        :param full_link_string (str): Markdown link in format `[link text](link URL)`. `link text` can be any \
        string. `link URL` must be a non-empty string in format `path/to/file#heading-id`.

        :raise TypeError: If `full_link_string` is not a string.
                ValueError: If `full_link_string` is an empty string.
                ValueError: If the URL part in `full_link_string` is empty or invalid format.
        """
        if not isinstance(full_link_string, str):
            raise TypeError('Markdown link must be a string.')
        if not full_link_string:
            raise ValueError('Markdown link must be a non-empty string.')

        link_text, link_url = MarkdownLink._split_full_link(full_link_string)
        if link_text:
            self._text = link_text
        else:
            raise ValueError('Cannot parse Markdown link text.')
        if not link_url:
            raise ValueError('Cannot parse Markdown link URL.')

        link_url_parts = MarkdownLink._split_url(link_url)
        if not link_url_parts:
            raise ValueError('Cannot parse link parts (path, file, and heading).')

        self._init_url_parts(link_url_parts)

    @property
    def url_path(self) -> str:
        return self._url_path

    @property
    def url_file(self) -> str:
        return self._url_file

    @property
    def url_heading(self) -> str:
        return self._url_heading

    @property
    def url(self):
        url = ''
        if self.url_path:
            url += self.url_path
        if self.url_file:
            url += self.url_file
        if self.url_heading:
            url += '#' + self.url_heading
        return url

    @property
    def text(self):
        return self._text

    def __str__(self) -> str:
        return self.url

    @property
    def type(self):
        if self.url_path is None:
            if self.url_file is None:
                if self.url_heading is not None:
                    return self.MarkdownLinkType.INBOUND
            else:
                return self.MarkdownLinkType.OUTBOUND
        elif "://" in self.url_path:
            return self.MarkdownLinkType.EXTERNAL
        else:
            if self.url_file is None:
                return self.MarkdownLinkType.EXTERNAL
            else:
                return self.MarkdownLinkType.OUTBOUND

    @classmethod
    def _split_full_link(cls, full_link_string: str) -> tuple[str | None, str | None]:
        link_text_match = re.search(constants.MARKDOWN_LINK_TEXT_PATTERN, full_link_string)
        link_url_match = re.search(constants.MARKDOWN_LINK_URL_PATTERN, full_link_string)

        if link_text_match:
            link_text = link_text_match.group(1)
        else:
            link_text = None

        if link_url_match:
            link_url = link_url_match.group(1)
        else:
            link_url = None
        return link_text, link_url

    @classmethod
    def _split_url(cls, url_string: str) -> tuple[str | None, str | None, str | None] | None:
        link_parts = re.match(constants.SPLIT_LINK_PATTERN, url_string)
        if link_parts:
            path, file, heading = None, None, None
            try:
                path = link_parts.group(1)
                file = link_parts.group(2) or None  # this is the only part that can be an empty string
                heading = link_parts.group(3)
            except IndexError:
                raise IndexError('Link parts contain less elements than expected (3).')
            finally:
                return path, file, heading
        else:
            return None

    def _init_url_parts(self, url_parts: tuple[str | None, str | None, str | None]) -> None:
        if url_parts[0]:
            self._url_path = url_parts[0].strip()
        else:
            self._url_path = None

        self._url_file = url_parts[1]

        if url_parts[2]:
            self._url_heading = url_parts[2].strip()
        else:
            self._url_heading = None

    class MarkdownLinkType(Enum):
        INBOUND = 'inbound'
        OUTBOUND = 'outbound'
        EXTERNAL = 'external'


if __name__ == "__main__":
    pass
