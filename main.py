from config import *
from parser import *

def run_action(config):
    dir = Dir(config["MAIN"]["root"])
    action = config["MAIN"]["action"]
    output = config["MAIN"]["output"]
    dir.scan_filenames(extension=config["MAIN"]["file_extension"])

    if action == Action.CHECK_LINKS.value:
        dir.parse_files()
        dir.check_internal_links()
        dir.check_external_links()
        if output == Output.CONSOLE.value:
            dir.print_broken_links()
        else:
            dir.fprint_broken_links()

    elif action == Action.SEARCH.value:
        str_to_find = input("Enter the string to find: ")
        dir.search(str_to_find, config["MAIN"]["output"])

    elif action == Action.PRINT_LINKS.value:
        dir.parse_files()
        if output == Output.CONSOLE.value:
            dir.print_all_links()
        else:
            dir.fprint_all_links()


config = set_config()
run_action(config)
