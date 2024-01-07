import re

# Matches a string with HTML comment tag: starts with '<!--', ends with '-->'.
COMMENTED_LINE_PATTERN = re.compile(r"<!--.+-->")

# Matches a string with any number of '#' symbols in the beginning and any characters after.
HEADING_PATTERN = re.compile(r"(^#+\s.[^{]+)")

# Matches any characters of a string between '{#' and '}' symbols.
HEADING_ID_PATTERN = re.compile(r"({#.+})$")

# Matches full Markdown link: a combination of '[any characters](any characters)'.
MARKDOWN_FULL_LINK_PATTERN = re.compile(r"(\[[^]]+]\([^)]+\))")

# Matches link URL in Markdown link: the part between '(' and ')' symbols.
MARKDOWN_LINK_URL_PATTERN = re.compile(r"\(([^)]+)\)")

# Matches link text in Markdown link: the part between '[' and ']' symbols.
MARKDOWN_LINK_TEXT_PATTERN = re.compile(r"\[([^)]+)]")

# Splits any string into 3 groups. 1 group includes any characters from the beginning to the '/' symbol.
# Equals to the file path. 2 group includes any characters from '/' symbol to the '#' symbol.
# Equals to the file. 3 group includes everything after '#' symbol. Equals to the heading.
SPLIT_LINK_PATTERN = re.compile(r"^(.*?/)?([^/#]*)(?:#(.*))?$")
