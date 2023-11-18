from pathlib import Path
import sys
import time

from parser import file as parsed_file


class Dir:
    def __init__(self, path):
        self.parsed_files = {}
        self.filenames = []
        self.path = path
        self.broken_internal_links = {}
        self.broken_external_links = {}

    def scan_filenames(self, extension=".mdx"):
        path = Path(self.path).absolute()
        self.filenames = list(path.glob(f'**/*{extension}'))

    def parse_files(self):
        if not self.filenames:
            return
        for filename in self.filenames:
            new_file = parsed_file.File(str(filename))
            new_file.parse_links()
            self.parsed_files[new_file.path_with_name] = new_file

    def check_internal_links(self):
        if not self.parsed_files:
            return
        for file in self.parsed_files.values():
            broken_links = file.check_internal_links()
            if broken_links:
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

    def search(self, string_to_search, output):
        if string_to_search == "":
            return
        search_result = {}
        found_matches = 0

        for filename in self.filenames:
            new_file = parsed_file.File(str(filename))
            occurrences_in_file = new_file.search(string_to_search)
            if occurrences_in_file:
                search_result[filename] = occurrences_in_file
                for (line, matches) in occurrences_in_file:
                    found_matches += matches

        if output == "console":
            if search_result:
                print(f"Search results for {string_to_search}")
                print(f"Found total: {found_matches} matches")
                for file in search_result.keys():
                    print(f"\nFile: {file}")
                    for (line_num, occurrences) in search_result[file]:
                        print(f"Line {line_num}: found {occurrences} occurrence(s)")

            else:
                print(f"{string_to_search} was not found.")

        elif output == "file":
            with open(time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime()) + f'-search-result-{string_to_search}.txt',
                      'w') \
                    as output_file:
                if search_result:
                    output_file.write(f"Search results for {string_to_search}\n")
                    output_file.write(f"Found total: {found_matches} matches\n")
                    for file in search_result.keys():
                        output_file.write(f"=============\nFile: {file}\n")
                        for (line_num, occurrences) in search_result[file]:
                            output_file.write(f"Line {line_num}: found {occurrences} occurrence(s)\n")

                else:
                    output_file.write(f"{string_to_search} was not found.\n")

    def print_broken_links(self):
        if not self.broken_external_links and not self.broken_internal_links:
            print("No broken links found")
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

        sys.exit("Found broken links!")

    def fprint_broken_links(self):
        with open(time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime()) + '-broken-links.txt', 'w') as output_file:
            if not self.broken_external_links and not self.broken_internal_links:
                output_file.write("No broken links found")
                return
            output_file.write("Broken internal links\n================")
            for file in self.broken_internal_links:
                if self.broken_internal_links[file]:
                    output_file.write(f"\nFile: {file}")
                    for (line, link) in self.broken_internal_links[file]:
                        output_file.write(f"\nLine {line}: not found {link}")
            output_file.write("\nBroken external links\n================")
            for file in self.broken_external_links:
                if self.broken_external_links[file]:
                    output_file.write(f"\nFile: {file}")
                    for (line, link) in self.broken_external_links[file]:
                        output_file.write(f"\nLine {line}: not found {link}")

    def print_all_links(self):
        if not self.parsed_files:
            return

        for file in self.parsed_files.values():
            file.print_all_links()

    def fprint_all_links(self):
        with open(time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime()) + '-all-links.txt', 'w') as output_file:

            if not self.parsed_files:
                output_file.write("No links were found.")
                return

            for file in self.parsed_files.values():
                output_file.write(f"\n=============\nFile: {file.path_with_name}")
                output_file.write(f"\nInbound links:")
                if file.inbound_links:
                    for inbound_link in file.inbound_links:
                        output_file.write(f"\n{inbound_link}")
                else:
                    output_file.write("\nNo inbound links found.")

                output_file.write(f"\nInternal links:")
                if file.internal_links:
                    for (line_num, internal_link) in file.internal_links:
                        output_file.write(f"\nLine {line_num}: {internal_link.heading}")
                else:
                    output_file.write("\nNo internal links found.")

                output_file.write("\nExternal links:")
                if file.external_links:
                    for (line_num, external_link) in file.external_links:
                        output_file.write(f"\nLine {line_num}: path: {external_link.path}, "
                                          f"file: {external_link.file}, "
                                          f"heading: {external_link.heading}")
                else:
                    output_file.write("\nNo external links found")

                output_file.write("\nOutside links:")
                if file.outside_links:
                    for (line_num, outside_link) in file.outside_links:
                        output_file.write(f"\nLine {line_num}: {outside_link}")
                else:
                    output_file.write("\nNo outside links found.")


if __name__ == "__main__":
    pass
