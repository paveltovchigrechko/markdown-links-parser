import argparse
from enum import Enum
from pathlib import Path
import configparser


class Output(Enum):
    CONSOLE = "console"
    FILE = "file"


class Action(Enum):
    CHECK_LINKS = "check_links"
    PRINT_LINKS = "print_links"
    SEARCH = "search"


CONFIG_NAME = "config.ini"
DEFAULT_CONFIG = configparser.ConfigParser()
DEFAULT_CONFIG['MAIN'] = {
    "root": "../doc-dev/docs",
    "file_extension": ".mdx",
    "output": Output.CONSOLE.value,
    "action": Action.CHECK_LINKS.value,
}


def set_config_from_args(arguments: argparse.Namespace) -> configparser.ConfigParser:
    config = configparser.ConfigParser()

    config.add_section('MAIN')
    for parameter in vars(arguments):
        config['MAIN'][parameter] = vars(arguments)[parameter]
    return config


def set_config(*, config_file=CONFIG_NAME, arguments=None) -> configparser.ConfigParser:
    # If there are passed arguments, use them to create configuration
    if arguments:
        config = set_config_from_args(arguments)
        return config

    # if there are no passed arguments, try to read configuration file
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except configparser.MissingSectionHeaderError:
        print("Configuration file misses sections. Using default configuration.")
        return DEFAULT_CONFIG

    if not config.sections():
        print("No configuration file found or configuration file is empty. Using default configuration.")
        return DEFAULT_CONFIG
    else:
        if "MAIN" not in config.sections():
            print("MAIN section is missing. Using default configuration.")
            return DEFAULT_CONFIG
        else:
            for obligatory_key in DEFAULT_CONFIG["MAIN"]:
                if obligatory_key not in config["MAIN"]:
                    print(f"Missing obligatory '{obligatory_key}' parameter: "
                          f"using value from default configuration ('{DEFAULT_CONFIG['MAIN'][obligatory_key]}')")
                    config["MAIN"][obligatory_key] = DEFAULT_CONFIG['MAIN'][obligatory_key]

                elif obligatory_key == "action" or obligatory_key == "output":
                    value = config["MAIN"][obligatory_key]
                    action_values = [item.value for item in Action]
                    output_values = [item.value for item in Output]
                    if value not in action_values and value not in output_values:
                        print(f"Key '{obligatory_key}' has incorrect value, "
                              f"using value from default configuration ('{DEFAULT_CONFIG['MAIN'][obligatory_key]}')")
                        config["MAIN"][obligatory_key] = DEFAULT_CONFIG['MAIN'][obligatory_key]

                elif obligatory_key == "root":
                    root_value = config["MAIN"][obligatory_key]
                    if root_value == "":
                        print(f"Key '{obligatory_key}' is empty, "
                              f"using value from default configuration ('{DEFAULT_CONFIG['MAIN'][obligatory_key]}')")
                        config["MAIN"][obligatory_key] = DEFAULT_CONFIG['MAIN'][obligatory_key]
                    else:
                        path = Path(config["MAIN"][obligatory_key]).absolute()
                        if not Path.exists(path) or not Path.is_dir(path):
                            print(f"Directory in '{obligatory_key}' was not found, "
                                  f"using value from default configuration ('{DEFAULT_CONFIG['MAIN'][obligatory_key]}')")
                            config["MAIN"][obligatory_key] = DEFAULT_CONFIG['MAIN'][obligatory_key]
    return config


if __name__ == "__main__":
    pass
