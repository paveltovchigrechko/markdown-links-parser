import re
# from typing import LiteralString

from app.utils import constants


def process_heading(heading_match: re.Match) -> str:
    raw_heading = heading_match.group().strip("# ").lower()
    heading_words = raw_heading.split()
    processed_words = []
    for word in heading_words:
        processed_word = word.strip("!?:()*")
        processed_words.append(processed_word)
    return "-".join(processed_words)


def process_heading_id(heading_id_match: re.Match):
    return heading_id_match.group().strip("{#}")


def is_commented_line(comment_pattern: re.compile, line: str) -> True | False:
    match = re.search(comment_pattern, line)
    if match:
        return True
    return False


def parse_heading(line: str):
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
