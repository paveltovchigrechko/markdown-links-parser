import configparser

CONFIG_NAME = "config.ini"
DEFAULT_CONFIG = configparser.ConfigParser()
DEFAULT_CONFIG['MAIN'] = {
    "root": ".",
    "file_extension": ".mdx",
    "output": "console",
    "action": "check_links",
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
                    print(f"Missing obligatory {obligatory_key} "
                          f"parameter: using value from default configuration ({DEFAULT_CONFIG['MAIN'][obligatory_key]})")
                    config["MAIN"][obligatory_key] = DEFAULT_CONFIG['MAIN'][obligatory_key]

    return config

if __name__ == "__main__":
    pass
