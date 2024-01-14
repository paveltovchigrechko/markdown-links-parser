"""
Utility functions used in other modules.
"""

import re

from app.utils import constants


def process_heading(heading_match: re.Match) -> str:
    """
    Accepts the re.Match for the Markdown heading (`# Some Markdown heading`) and returns the string version of heading words concatenated with `-`.
    :param heading_match: The re.Match object for a Markdown heading.
    :return: A single string of all heading words concatenated with `-` (`some-markdown-heading`).
    """
    raw_heading = heading_match.group().strip("# ").lower()
    heading_words = raw_heading.split()
    processed_words = []
    for word in heading_words:
        processed_word = word.strip("!?:()*")
        processed_words.append(processed_word)
    return "-".join(processed_words)


def process_heading_id(heading_id_match: re.Match) -> str:
    """
    Strips the `#` from a MArkdown heading match.
    :param heading_id_match: The re.Match object for a Markdown heading.
    :return: The Markdown heading string without leading `#`.
    """
    return heading_id_match.group().strip("{#}")


def is_commented_line(comment_pattern: re.compile, line: str) -> True | False:
    """
    Checks if a line is commented (i.e. matches a passed pattern).
    :param comment_pattern: The pattern for a commented line.
    :param line: The line string.
    :return: True if the `line` matches the `comment_pattern`, False otherwise.
    """
    match = re.search(comment_pattern, line)
    if match:
        return True
    return False


def parse_heading(line: str) -> tuple[None, str] | tuple[str, None] | tuple[None, None]:
    """
    Parses a Markdown line and returns the heading or heading ID (`{#heading-id}`) if exists.
    :param line: The line string.
    :return: Return a tuple where the first element is a heading string, and the second is a heading ID.
    If a heading is not parsed, both elements in tuple are None.
    If a heading is parsed, but a heading ID is not, return `tuple[str, None]`.
    If a heading ID is parsed, return `tuple[None, str]`.
    """
    match_heading = re.search(constants.HEADING_PATTERN, line)

    if match_heading:
        processed_heading = process_heading(match_heading)
        match_heading_id = re.search(constants.HEADING_ID_PATTERN, line)
        if match_heading_id:
            processed_heading_id = process_heading_id(match_heading_id)
            return None, processed_heading_id
        return processed_heading, None
    else:
        return None, None
