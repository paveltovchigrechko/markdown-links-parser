import config

import os
import unittest



class ConfigTests(unittest.TestCase):
    def test_read_correct_config_file(self):
        print("test_read_correct_config_file")
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[MAIN]\nroot: .\nfile_extension: .mdx\noutput: console\naction: check_links''')

        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

        os.remove(config.CONFIG_NAME)

    def test_no_config_file(self):
        print("test_no_config_file")
        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

    def test_config_file_without_sections(self):
        print("test_config_file_without_sections")
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''root: .\nfile_extension: .mdx\noutput: console\naction: check_links''')

        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

        os.remove(config.CONFIG_NAME)

    def test_config_file_empty(self):
        print("test_config_file_empty")
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.close()

        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

        os.remove(config.CONFIG_NAME)

    def test_config_file_without_main_section(self):
        print("test_config_file_without_main_section")
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[SECTION]\nroot: .\nfile_extension: .mdx\noutput: console\naction: check_links''')

        cfg = config.set_config()
        self.assertEqual(cfg, config.DEFAULT_CONFIG)

        os.remove(config.CONFIG_NAME)

    def test_config_file_without_obligatory_keys(self):
        print("test_config_file_without_obligatory_keys")
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[MAIN]\nparameter: .\nextension: .mdx\noutput_result: file\nfunc_action: check_links''')

        cfg = config.set_config()
        for obligatory_key in config.DEFAULT_CONFIG["MAIN"]:
            self.assertTrue(obligatory_key in cfg["MAIN"])
            self.assertEqual(cfg["MAIN"][obligatory_key], config.DEFAULT_CONFIG["MAIN"][obligatory_key])

        os.remove(config.CONFIG_NAME)

    def test_config_file_with_wrong_value_in_enum_key(self):
        print("test_config_file_with_wrong_enum__in_obligatory_key")
        with open(config.CONFIG_NAME, mode='w') as config_file:
            config_file.write('''[MAIN]\nroot: .\nfile_extension: .mdx\noutput: print\naction: value''')

        cfg = config.set_config()
        self.assertEqual(cfg["MAIN"]["output"], config.DEFAULT_CONFIG["MAIN"]["output"])
        self.assertEqual(cfg["MAIN"]["action"], config.DEFAULT_CONFIG["MAIN"]["action"])

        os.remove(config.CONFIG_NAME)

if __name__ == "__main__":
    unittest.main()