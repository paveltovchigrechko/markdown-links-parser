from config.config import *
import parser.dir as dir

def run_action(config):
    directory = dir.Dir(config["MAIN"]["root"])
    action = config["MAIN"]["action"]
    output = config["MAIN"]["output"]
    directory.scan_filenames(extension=config["MAIN"]["file_extension"])

    if action == Action.CHECK_LINKS.value:
        directory.parse_files()
        directory.check_internal_links()
        directory.check_external_links()
        if output == Output.CONSOLE.value:
            directory.print_broken_links()
        else:
            directory.fprint_broken_links()

    elif action == Action.SEARCH.value:
        str_to_find = input("Enter the string to find: ")
        directory.search(str_to_find, config["MAIN"]["output"])

    elif action == Action.PRINT_LINKS.value:
        directory.parse_files()
        if output == Output.CONSOLE.value:
            directory.print_all_links()
        else:
            directory.fprint_all_links()


config = set_config()
run_action(config)
