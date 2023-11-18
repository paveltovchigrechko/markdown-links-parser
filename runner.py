import config.config
import parser.dir


def run_parser(configuration_file):
    directory = parser.dir.Dir(configuration_file["MAIN"]["root"])
    action = configuration_file["MAIN"]["action"]
    output = configuration_file["MAIN"]["output"]
    directory.scan_filenames(extension=configuration_file["MAIN"]["file_extension"])

    if action == config.config.Action.CHECK_LINKS.value:
        directory.parse_files()
        directory.check_internal_links()
        directory.check_external_links()
        if output == config.config.Output.CONSOLE.value:
            directory.print_broken_links()
        else:
            directory.fprint_broken_links()

    elif action == config.config.Action.SEARCH.value:
        str_to_find = input("Enter the string to find: ")
        directory.search(str_to_find, configuration_file["MAIN"]["output"])

    elif action == config.config.Action.PRINT_LINKS.value:
        directory.parse_files()
        if output == config.config.Output.CONSOLE.value:
            directory.print_all_links()
        else:
            directory.fprint_all_links()
