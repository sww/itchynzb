import binascii
import eventlet
import os
import shutil
import StringIO
import struct
import unittest
import download
import fakeserver

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
        # Start the test server.
        self.server = eventlet.spawn(fakeserver.start)

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

        self.nzb = StringIO.StringIO("""<?xml version="1.0" encoding="iso-8859-1" ?>
          <!DOCTYPE nzb PUBLIC "-//newzBin//DTD NZB 1.0//EN" "http://www.newzbin.com/DTD/nzb/nzb-1.0.dtd">
          <nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">
            <file poster="some poster@unknown.com" date="1298537493" subject="gpl.txt">
              <groups>
                <group>alt.cool</group>
              </groups>
              <segments>
                <segment bytes="18264" number="1">gplsegment@something.com</segment>
              </segments>
            </file>
           </nzb>""")

        self.nzb2 = StringIO.StringIO("""<?xml version="1.0" encoding="iso-8859-1" ?>
          <!DOCTYPE nzb PUBLIC "-//newzBin//DTD NZB 1.0//EN" "http://www.newzbin.com/DTD/nzb/nzb-1.0.dtd">
          <nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">
            <file poster="some poster@unknown.com" date="1298537493" subject="gut96back.jpg">
              <groups>
                <group>alt.cool</group>
              </groups>
              <segments>
                <segment bytes="255937" number="1">prjtgtnbrg01@something.com</segment>
                <segment bytes="150445" number="2">prjtgtnbrg02@something.com</segment>
              </segments>
            </file>
           </nzb>""")

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
        self.server.kill()

if __name__ == '__main__':
    unittest.main()
