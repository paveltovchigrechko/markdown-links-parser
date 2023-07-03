from config import *
from parser import *

def run_action(config):
    dir = Dir(config["MAIN"]["root"])
    dir.scan_filenames(extension=config["MAIN"]["file_extension"])

    if config["MAIN"]["action"] == Action.CHECK_LINKS.value:
        dir.parse_files()
        dir.check_internal_links()
        dir.check_external_links()
        if config["MAIN"]["output"] == Output.CONSOLE.value:
            dir.print_broken_links()
        else:
            dir.fprint_broken_links()

    elif config["MAIN"]["action"] == Action.SEARCH.value:
        str_to_find = input("Enter the string to find: ")
        dir.search(str_to_find, config["MAIN"]["output"])

    elif config["MAIN"]["action"] == Action.PRINT_LINKS.value:
        dir.parse_files()
        if config["MAIN"]["output"] == Output.CONSOLE.value:
            dir.print_all_links()
        else:
            dir.fprint_all_links()


config = set_config()
run_action(config)
