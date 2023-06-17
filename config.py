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
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_NAME)
    except configparser.MissingSectionHeaderError:
        print("Configuration file misses sections. Using default configuration.")
        config = DEFAULT_CONFIG

    if not config.sections():
        print("Configuration file is empty. Using default configuration.")
        config = DEFAULT_CONFIG
    else:
        if "MAIN" not in config.sections():
            print("MAIN section is missing. Using default configuration.")
            config = DEFAULT_CONFIG
        else:
            for obligatory_key in DEFAULT_CONFIG["MAIN"]:
                if obligatory_key not in config["MAIN"]:
                    print(f"Missing obligatory {obligatory_key} parameter: "
                          f"using value from default configuration ({DEFAULT_CONFIG['MAIN'][obligatory_key]})")
                    config["MAIN"][obligatory_key] = DEFAULT_CONFIG['MAIN'][obligatory_key]
                elif obligatory_key == "action" or obligatory_key == "output":
                    value = config["MAIN"][obligatory_key]
                    print(value)
                    action_values = [item.value for item in Action]
                    print(action_values)
                    output_values = [item.value for item in Output]
                    print(output_values)
                    if value not in action_values or value not in output_values:
                        print(f"Key {obligatory_key} has incorrect value, "
                              f"using value from default configuration ({DEFAULT_CONFIG['MAIN'][obligatory_key]})")
                        config["MAIN"][obligatory_key] = DEFAULT_CONFIG['MAIN'][obligatory_key]
    return config

if __name__ == "__main__":
    pass
