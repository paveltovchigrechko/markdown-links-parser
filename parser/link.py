import re

# Splits any string into 3 groups. 1 group includes any characters from the beginning to the '/' symbol.
# Equals to the file path. 2 group includes any characters from '/' symbol to the '#' symbol.
# Equals to the file. 3 group includes everything after '#' symbol. Equals to the heading.
SPLIT_LINK_PATTERN = re.compile(r"^(.*?/)?([^/#]*)(?:#(.*))?$")

class Link:
    def __init__(self, link_string):
        link_parts = re.match(SPLIT_LINK_PATTERN, link_string)
        self.path = link_parts.group(1)
        self.file = link_parts.group(2)
        self.heading = link_parts.group(3)

    def __str__(self):
        link_string = ""
        if self.path is not None:
            link_string += self.path
        if self.file is not None:
            link_string += self.file
        if self.heading is not None:
            link_string += "#" + self.heading
        return link_string


if __name__ == "__main__":
    pass