import os
import shutil
import threading
import unittest

import itchy
import fakeserver

fakeserver.DEBUG = False
server = threading.Thread(target=fakeserver.start)
server.setDaemon(True)
server.start()

class Options(object):

    def __init__(self, config_file='', debug=False, pattern=[], par2=False):
        self.config_file = config_file
        self.debug = debug
        self.pattern = pattern
        self.par2 = par2

class TestItchy(unittest.TestCase):

    def setUp(self):
        self.download_dir = 'testdownloads'
        self.temp_dir = 'testtemp'
        self.files_dir = 'testfiles'

        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        # Copy over the zip file to avoid overwriting files.
        try:
            os.mkdir(self.files_dir)
        except OSError:
            pass

        os.mkdir(self.download_dir)
        os.mkdir(self.temp_dir)

        self.options = Options('files/settings/test.json', pattern=[])
        self.settings = {
            'host': 'localhost',
            'username': 'testuser',
            'password': 'testpass',
            'port': 5000,
            'connections': 1,
            'download_path': self.download_dir,
            'temp_dir': self.temp_dir,
            'skip_regex': []
        }

    def test_zip_download(self):
        """Test zip downloads."""
        shutil.copy('files/nzb/nzbs.zip', self.files_dir)
        # OptionParser's args come in a list.
        itchy.main([os.path.join(self.files_dir, 'nzbs.zip')], self.options)
        self.assertTrue(os.path.exists('testdownloads/gpl/gpl.txt'))
        self.assertTrue(os.path.exists('testdownloads/gutenberg/gut96back.jpg'))
        self.assertEqual(os.listdir('testtemp'), [])

    def test_multiple_downloads(self):
        """Test a directory download of multiple NZB files."""
        shutil.copy('files/nzb/gpl.nzb', self.files_dir)
        shutil.copy('files/nzb/gutenberg.nzb', self.files_dir)
        itchy.main([self.files_dir], self.options)
        self.assertTrue(os.path.exists('testdownloads/gpl/gpl.txt'))
        self.assertTrue(os.path.exists('testdownloads/gutenberg/gut96back.jpg'))
        self.assertEqual(os.listdir('testtemp'), [])

    def tearDown(self):
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        if os.path.exists(self.files_dir):
            shutil.rmtree(self.files_dir)

if __name__ == '__main__':
    unittest.main()
