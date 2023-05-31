from pathlib import Path
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
MARKDOWN_LINK_PATTERN = re.compile(r"\(([^)]+)\)")
# Splits any string into 3 groups. 1 group includes any characters from the beginning to the '/' symbol.
# Equals to the file path. 2 group includes any characters from '/' symbol to the '#' symbol.
# Equals to the file. 3 group includes everything after '#' symbol. Equals to the heading.
SPLIT_LINK_PATTERN = re.compile(r"^(.*?\/)?([^\/#]*)(?:#(.*))?$")


class MarkdownLink:
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


class File:
    def __init__(self, path_to_file):
        path_parts = re.match(SPLIT_LINK_PATTERN, path_to_file)
        self.path = path_parts.group(1)
        self.name = path_parts.group(2)
        self.path_with_name = self.path + self.name
        self.inbound_links = {}
        self.internal_links = []
        self.external_links = []
        self.outside_links = []

    def parse_links(self, ignore_commented_lines=True):
        with open(self.path_with_name) as file:
            inbound_links_list = []

            def process_heading (heading_match):
                raw_heading = heading_match.group().strip("# ").lower()
                heading_words = raw_heading.split()
                processed_words = []
                for word in heading_words:
                    processed_word = word.strip("!?:()*")
                    processed_words.append(processed_word)
                return "-".join(processed_words)
                # return "-".join(heading_match.group().strip("# ").lower().split())

            def process_heading_id (heading_id_match):
                return heading_id_match.group().strip("{#}")

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
                        link = MarkdownLink(re.search(MARKDOWN_LINK_PATTERN, full_link).group(1))
                        if link.path is None:
                            # If a link has no path and file, then it is internal link
                            if link.file == '':
                                self.internal_links.append((line_num, link))
                            else:
                                self.external_links.append((line_num, link))
                        # If a link contains protocol, it leads outside
                        elif "://" in link.path:
                            self.outside_links.append((line_num, link))
                        else:
                            self.external_links.append((line_num, link))

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
        print(f"\n********\nFile:", self.path_with_name)
        print(f"Inbound links:")
        for inbound_link in self.inbound_links:
            print(f"{inbound_link}")
        print(f"========\nInternal links:")
        for (line_num, internal_link) in self.internal_links:
            print(f"Line {line_num}: {internal_link.heading}")
        print(f"========\nExternal links:")
        for (line_num, external_link) in self.external_links:
            print(
                f"Line {line_num}: path: {external_link.path}, file: {external_link.file}, heading: {external_link.heading}")
        print(f"========\nOutside links:")
        for (line_num, outside_link) in self.outside_links:
            print(f"Line {line_num}: path: {outside_link}")


class Dir:
    def __init__(self, path):
        self.parsed_files = {}
        self.filenames = []
        self.path = path
        self.broken_internal_links = {}
        self.broken_external_links = {}

    def scan_filenames(self, extension=".mdx"):
        path = Path(self.path)
        self.filenames = list(path.glob(f'**/*{extension}'))

    def parse_files(self):
        if not self.filenames:
            return
        for filename in self.filenames:
            new_file = File(str(filename))
            new_file.parse_links()
            self.parsed_files[new_file.path_with_name] = new_file

    def check_internal_links(self):
        if not self.parsed_files:
            return
        for file in self.parsed_files.values():
            broken_links = file.check_internal_links()
            self.broken_internal_links[file.path_with_name] = broken_links

    def check_external_links(self):
        if not self.parsed_files:
            return
        for file in self.parsed_files.values():
            broken_external_links = []
            start_path = Path(file.path)
            for (line_num, external_link) in file.external_links:
                if external_link.path is None:
                    relative_path = external_link.file
                else:
                    relative_path = external_link.path + external_link.file
                reference_path = Path.joinpath(start_path, relative_path)
                if Path.exists(reference_path):
                    if external_link.heading:
                        file_path = str(reference_path.resolve())
                        if external_link.heading not in self.parsed_files[file_path].inbound_links:
                            broken_external_links.append((line_num, external_link))
                    else:
                        continue
                else:
                    broken_external_links.append((line_num, external_link))

            if broken_external_links:
                self.broken_external_links[file.path_with_name] = broken_external_links

    def search(self, string_to_search):
        search_result = {}

        for filename in self.filenames:
            new_file = File(str(filename))
            occurrences_in_file = new_file.search(string_to_search)
            if occurrences_in_file:
                search_result[filename] = occurrences_in_file

        if search_result:
            print(f"Search results for {string_to_search}")
            for file in search_result.keys():
                print(f"File: {file}")
                for (line_num, occurrences) in search_result[file]:
                    print(f"Line {line_num}: found {occurrences} occurrence(s)")

    def print_broken_links(self):
        if not self.broken_external_links and not self.broken_internal_links:
            return
        print("Broken internal links\n================")
        for file in self.broken_internal_links:
            if self.broken_internal_links[file]:
                print(f"\nFile: {file}")
                for (line, link) in self.broken_internal_links[file]:
                    print(f"Line {line}: not found {link}")
        print("\nBroken external links\n================")
        for file in self.broken_external_links:
            if self.broken_external_links[file]:
                print(f"\nFile: {file}")
                for (line, link) in self.broken_external_links[file]:
                    print(f"Line {line}: not found {link}")

docs_directory = "/home/pavel/dev/python/markdown-links-parser/docs-test"
dev_directory = "/home/pavel/dev/python/markdown-links-parser/dev-docs-test"
directory = docs_directory
dir = Dir(directory)
dir.scan_filenames()
search = dir.search("UNLIMIT")
dir.parse_files()
dir.check_internal_links()
dir.check_external_links()
dir.print_broken_links()
