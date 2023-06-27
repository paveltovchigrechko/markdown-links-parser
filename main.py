from config import *
from parser import *

config = set_config()

dir = Dir(config["MAIN"]["root"])
dir.scan_filenames(extension=config["MAIN"]["file_extension"])

print(Path(dir.path).absolute())

if config["MAIN"]["action"] == Action.CHECK_LINKS.value:
    dir.parse_files()
    dir.check_internal_links()
    dir.check_external_links()
    dir.print_broken_links()

elif config["MAIN"]["action"] == Action.SEARCH.value:
    str_to_find = input("Enter the string to find: ")
    dir.search(str_to_find)

elif config["MAIN"]["action"] == Action.PRINT_LINKS.value:
    dir.parse_files()
    dir.print_all_links()
