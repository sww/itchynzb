import os
import unittest
import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        # self.keys = [
        #     'host',
        #     'username',
        #     'password',
        #     'port',
        #     'connections',
        #     'download_dir',
        #     'temp_dir',
        #     'skip_regex'
        # ]

        self.bad_config = 'bad_config.conf'
        self.config = 'config.conf'

        if os.path.exists(self.bad_config):
            os.remove(self.bad_config)
        if os.path.exists(self.config):
            os.remove(self.config)
       
        with open(self.bad_config, 'w') as bc:
            bc.write("""{
                "host": "localhost",
                "username": "user",
                "password": "pass",
                "port": 5000,
                "connections": 1,
                "download_path": "downloads",
                "temp_dir": "temp",
                "skip_regex": [".*\\\.par2", ".*\\\.avi(?!\\\.)", ".*\\\.nzb"]
            }""")

        with open(self.config, 'w') as cfg:
            cfg.write("""{
                "host": "localhost",
                "username": "user",
                "password": "pass",
                "port": 5000,
                "connections": 1,
                "download_dir": "downloads",
                "temp_dir": "temp",
                "skip_regex": [".*\\\.par2", ".*\\\.avi(?!\\\.)", ".*\\\.nzb"]
            }""")

    def test_config(self):
        cfg = config.read_config(self.config)
        self.assertEqual(cfg['host'], 'localhost')

    def test_raises(self):
        """Test that the config module will raise an exception when missing a key."""
        self.assertRaises(IOError, config.read_config, 'No Such File')
        self.assertRaises(KeyError, config.read_config, self.bad_config)

    def tearDown(self):
        if os.path.exists(self.bad_config):
            os.remove(self.bad_config)
        if os.path.exists(self.config):
            os.remove(self.config)

if __name__ == '__main__':
    unittest.main()
