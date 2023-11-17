import re

from parser import link

# Matches a string with HTML comment tag: starts with '<!--', ends with '-->'.
COMMENTED_LINE_PATTERN = re.compile(r"<!--.+-->")
# Matches a string with any number of '#' symbols in the beginning and any characters after.
HEADING_PATTERN = re.compile(r"(^#+\s.[^{]+)")
# Matches any characters of a string between '{#' and '}' symbols.
HEADING_ID_PATTERN = re.compile(r"({#.+})$")
# Matches full Markdown link: a combination of '[any characters](any characters)'.
MARKDOWN_FULL_LINK_PATTERN = re.compile(r"(\[[^]]+]\([^)]+\))")
# Matches link URL in Markdown link: the part between '(' and ')' symbols.
MARKDOWN_LINK_PATTERN = re.compile(r"\(([^)]+)\)")


class File:
    def __init__(self, path_to_file):
        path_parts = re.match(link.SPLIT_LINK_PATTERN, path_to_file)
        self.path = path_parts.group(1)
        self.name = path_parts.group(2)
        self.path_with_name = self.path + self.name
        self.inbound_links = {}
        self.internal_links = []
        self.external_links = []
        self.outside_links = []

    def parse_links(self, ignore_commented_lines=True):
        with open(self.path_with_name) as file:
            def process_heading(heading_match):
                raw_heading = heading_match.group().strip("# ").lower()
                heading_words = raw_heading.split()
                processed_words = []
                for word in heading_words:
                    processed_word = word.strip("!?:()*")
                    processed_words.append(processed_word)
                return "-".join(processed_words)

            def process_heading_id(heading_id_match):
                return heading_id_match.group().strip("{#}")

            inbound_links_list = []

            for (line_num, line) in enumerate(file, start=1):
                if ignore_commented_lines:
                    # If a line is commented, ignore it
                    commented_line = re.search(COMMENTED_LINE_PATTERN, line)
                    if commented_line:
                        continue

                # Parsing headings and heading IDs
                match_heading = re.search(HEADING_PATTERN, line)
                if match_heading:
                    processed_heading = process_heading(match_heading)
                    inbound_links_list.append(processed_heading)
                    match_heading_id = re.search(HEADING_ID_PATTERN, line)
                    if match_heading_id:
                        processed_heading_id = process_heading_id(match_heading_id)
                        inbound_links_list.append(processed_heading_id)

                # Parsing Markdown links only if there is no heading in line
                else:
                    # Find all full Markdown links in a line
                    full_markdown_links = re.findall(MARKDOWN_FULL_LINK_PATTERN, line)
                    for full_link in full_markdown_links:
                        new_link = link.Link(re.search(MARKDOWN_LINK_PATTERN, full_link).group(1))
                        if new_link.path is None:
                            # If a link has no path and file, then it is internal link
                            if new_link.file == '':
                                self.internal_links.append((line_num, new_link))
                            else:
                                self.external_links.append((line_num, new_link))
                        # If a link contains protocol, it leads outside
                        elif "://" in new_link.path:
                            self.outside_links.append((line_num, new_link))
                        else:
                            self.external_links.append((line_num, new_link))

        if inbound_links_list:
            self.inbound_links = set(inbound_links_list)

    def check_internal_links(self):
        if not self.internal_links:
            return []
        broken_internal_links = []
        for (line_num, internal_link) in self.internal_links:
            if internal_link.heading not in self.inbound_links:
                broken_internal_links.append((line_num, internal_link))
        return broken_internal_links

    def search(self, string_to_search):
        lower_string = string_to_search.lower()
        search_matches = []
        with open(self.path_with_name) as file:
            for (line_num, line) in enumerate(file, start=1):
                lower_line = line.lower()
                occurrences = re.findall(lower_string, lower_line)
                if occurrences:
                    search_matches.append((line_num, len(occurrences)))
        return search_matches

    def print_all_links(self):
        print("\nFile:", self.path_with_name)
        self.print_inbound_links()
        self.print_internal_links()
        self.print_external_links()
        self.print_outside_links()

    def print_inbound_links(self):
        print(f"\nInbound links:")
        if self.inbound_links:
            for inbound_link in self.inbound_links:
                print(f"{inbound_link}")
        else:
            print("No inbound links found.")

    def print_internal_links(self):
        print(f"\nInternal links:")
        if self.internal_links:
            for (line_num, internal_link) in self.internal_links:
                print(f"Line {line_num}: {internal_link.heading}")
        else:
            print("No internal links found.")

    def print_external_links(self):
        print("\nExternal links:")
        if self.external_links:
            for (line_num, external_link) in self.external_links:
                print(f"Line {line_num}: path: {external_link.path}, "
                      f"file: {external_link.file}, "
                      f"heading: {external_link.heading}")
        else:
            print("No external links found")

    def print_outside_links(self):
        print("\nOutside links:")
        if self.outside_links:
            for (line_num, outside_link) in self.outside_links:
                print(f"Line {line_num}: {outside_link}")
        else:
            print("No outside links found.")


if __name__ == "__main__":
    pass
