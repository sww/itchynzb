import unittest
import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.bad_config = 'files/settings/bad_config.json'
        self.config = 'files/settings/config.json'

    def test_config(self):
        cfg = config.read_config(self.config)
        self.assertEqual(cfg['host'], 'localhost')

    def test_raises(self):
        """Test that the config module will raise an exception when missing a key."""
        self.assertRaises(IOError, config.read_config, 'No Such File')
        self.assertRaises(KeyError, config.read_config, self.bad_config)

if __name__ == '__main__':
    unittest.main()
