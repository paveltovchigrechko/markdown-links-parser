import os
import unittest

from config import config


class ConfigTests(unittest.TestCase):
    def test_correct_config_file(self):
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[MAIN]\nroot: .\nfile_extension: .mdx\noutput: console\naction: check_links''')

        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

        os.remove(config.CONFIG_NAME)

    def test_correct_config_with_additional_keys(self):
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[MAIN]\nroot: .\nfile_extension: .mdx\noutput: console\naction: check_links\nfirst_parameter: value_01\n
            second_parameter: value_02\nthird_parameter: value_03\nforth_parameter: value_04''')

        cfg = config.set_config()
        for obligatory_key in config.DEFAULT_CONFIG["MAIN"]:
            self.assertTrue(obligatory_key in cfg["MAIN"])

        os.remove(config.CONFIG_NAME)

    def test_no_config_file(self):
        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

    def test_config_file_without_sections(self):
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''root: .\nfile_extension: .mdx\noutput: console\naction: check_links''')

        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

        os.remove(config.CONFIG_NAME)

    def test_config_file_empty(self):
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.close()

        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

        os.remove(config.CONFIG_NAME)

    def test_config_file_without_main_section(self):
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[SECTION]\nroot: .\nfile_extension: .mdx\noutput: console\naction: check_links''')

        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

        os.remove(config.CONFIG_NAME)

    def test_config_file_without_obligatory_keys(self):
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[MAIN]\nparameter: .\nextension: .mdx\noutput_result: file\nfunc_action: check_links''')

        cfg = config.set_config()
        for obligatory_key in config.DEFAULT_CONFIG["MAIN"]:
            self.assertTrue(obligatory_key in cfg["MAIN"])
            self.assertEqual(cfg["MAIN"][obligatory_key], config.DEFAULT_CONFIG["MAIN"][obligatory_key])

        os.remove(config.CONFIG_NAME)

    def test_config_file_with_wrong_value_in_enum_key(self):
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[MAIN]\nroot: .\nfile_extension: .mdx\noutput: print\naction: value''')

        cfg = config.set_config()
        self.assertEqual(cfg["MAIN"]["output"], config.DEFAULT_CONFIG["MAIN"]["output"])
        self.assertEqual(cfg["MAIN"]["action"], config.DEFAULT_CONFIG["MAIN"]["action"])

        os.remove(config.CONFIG_NAME)

    def test_config_file_with_empty_root(self):
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[MAIN]\nroot: \nfile_extension: .mdx\noutput: file\naction: check_links''')

        cfg = config.set_config()
        self.assertEqual(cfg["MAIN"]["root"], config.DEFAULT_CONFIG["MAIN"]["root"])

        os.remove(config.CONFIG_NAME)

    def test_config_file_with_root_not_directory(self):
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[MAIN]\nroot: ./test_config.py\nfile_extension: .mdx\noutput: file\naction: check_links''')

        cfg = config.set_config()
        self.assertEqual(cfg["MAIN"]["root"], config.DEFAULT_CONFIG["MAIN"]["root"])

        os.remove(config.CONFIG_NAME)


if __name__ == "__main__":
    unittest.main()
