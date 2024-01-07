import app.config.config as config
from app.models.directory import Directory


def run_parser(configuration_file):
    directory = Directory(configuration_file["MAIN"]["root"])
    action = configuration_file["MAIN"]["action"]
    # output = configuration_file["MAIN"]["output"]
    directory.scan_files_by_extension(file_extensions=[configuration_file["MAIN"]["file_extension"]])

    if action == config.Action.CHECK_LINKS.value:
        directory.init_files()
        broken_links = directory.validate_markdown_links()
        if broken_links:
            print()
            for file, links in broken_links.items():
                print(f'File: {file}')
                for line, broken_link in links:
                    print(f'Line {line}: not found "{broken_link.url}"')
                print('======================\n')
        else:
            print('No broken links found.')
        # if output == config.config.Output.CONSOLE.value:
        #     directory.print_broken_links()
        # else:
        #     directory.fprint_broken_links()

    # elif action == config.Action.SEARCH.value:
    #     str_to_find = input("Enter the string to find: ")
        # directory.search(str_to_find, configuration_file["MAIN"]["output"])

    # elif action == config.Action.PRINT_LINKS.value:
    #     directory.parse_files()
    #     if output == config.config.Output.CONSOLE.value:
    #         directory.print_all_links()
    #     else:
    #         directory.fprint_all_links()


if __name__ == "__main__":
    pass
