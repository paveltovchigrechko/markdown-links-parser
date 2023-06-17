from enum import Enum
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
    "root": ".",
    "file_extension": ".mdx",
    "output": Output.CONSOLE.value,
    "action": Action.CHECK_LINKS.value,
}

def set_config():
    # TODO: check if 'root' is path and is not empty
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_NAME)
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
    return config

if __name__ == "__main__":
    pass
