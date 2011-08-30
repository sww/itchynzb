import os
import shutil
import StringIO
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

        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

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

    def test_zip_download(self):
        """Test zip downloads."""
        itchy.main('files/nzb/nzbs.zip', self.options)
        self.assertTrue(os.path.exists('testdownloads/gpl/gpl.txt'))
        self.assertTrue(os.path.exists('testdownloads/gutenberg/gut96back.jpg'))
        self.assertEqual(os.listdir('testtemp'), [])

    def test_multiple_downloads(self):
        """Test a directory download of multiple NZB files."""
        pass

    def tearDown(self):
        if os.path.exists(self.download_dir):
            shutil.rmtree(self.download_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

if __name__ == '__main__':
    unittest.main()
