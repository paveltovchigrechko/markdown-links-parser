import app.config.config as config
from app.models.directory import Directory


def run_parser(configuration_file):
    directory = Directory(configuration_file["MAIN"]["root"])
    action = configuration_file["MAIN"]["action"]
    # output = configuration_file["MAIN"]["output"]
    directory.scan_files_by_extension(file_extensions=[configuration_file["MAIN"]["file_extension"]])

    directory.init_files()
    if action == config.Action.CHECK_LINKS.value:
        broken_links = directory.validate_markdown_links()
        if broken_links:
            print('\nFound broken links!')
            for file, links in broken_links.items():
                print(f'File: {file}')
                for line, broken_link in links:
                    print(f'Line {line}: not found "{broken_link.url}"')
                print('======================\n')
        else:
            print('No broken links found.')
    elif action == config.Action.SEARCH.value:
        str_to_find = input("Enter the string to find: ")
        search_results = directory.search(str_to_find)
        if search_results:
            print(f'Search results for {str_to_find}:\n')
            for file, results in search_results.items():
                print(f'File: {file}')
                for line, occurence in results:
                    print(f'Line {line}: found {occurence} occurences.')
                print('======================\n')
        else:
            print(f'{str_to_find} was not found.')


if __name__ == "__main__":
    pass
