import binascii
import os
import shutil
import struct
import threading
import unittest

import download
import fakeserver

fakeserver.DEBUG = False
server = threading.Thread(target=fakeserver.start)
server.setDaemon(True)
server.start()

class TestDownload(unittest.TestCase):

    def setUp(self):
        self.download_dir = 'testdownloads'
        self.temp_dir = 'testtemp'

        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        os.mkdir(self.download_dir)
        os.mkdir(self.temp_dir)

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

        self.nzb = 'files/nzb/gpl.nzb'
        self.nzb2 = 'files/nzb/gutenberg.nzb'

    def test_download(self):
        """Test a download of a single segment file."""
        download.start(self.nzb, self.settings)
        self.assertTrue(os.path.exists(os.path.join(self.download_dir, 'gpl.txt')))
        # Make sure it's being going where it's supposed to go.
        self.assertEqual(os.listdir(self.download_dir), ['gpl.txt'])
        # Make sure we're cleaning up after ourselves.
        self.assertEqual(os.listdir(self.temp_dir), [])

        with open(os.path.join(self.download_dir, 'gpl.txt')) as f:
            data = f.read()
        checksum = binascii.hexlify(struct.pack('!l', binascii.crc32(data)))
        self.assertEqual(checksum, 'a0305209')

    def test_download2(self):
        """Test a download of a multiple segment file."""
        download.start(self.nzb2, self.settings)
        self.assertTrue(os.path.exists(os.path.join(self.download_dir, 'gut96back.jpg')))
        # Make sure it's being going where it's supposed to go.
        self.assertEqual(os.listdir(self.download_dir), ['gut96back.jpg'])
        # Make sure we're cleaning up after ourselves.
        self.assertEqual(os.listdir(self.temp_dir), [])

        with open(os.path.join(self.download_dir, 'gut96back.jpg')) as f:
            data = f.read()
        checksum = binascii.hexlify(struct.pack('!l', binascii.crc32(data)))
        self.assertEqual(checksum, '82fe6b72')

    def tearDown(self):
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
