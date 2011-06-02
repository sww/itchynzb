import StringIO
import unittest
from parser import parse_nzb

class TestParser(unittest.TestCase):
    def setUp(self):
        self.nzb = StringIO.StringIO("""<?xml version="1.0" encoding="iso-8859-1" ?>
          <!DOCTYPE nzb PUBLIC "-//newzBin//DTD NZB 1.0//EN" "http://www.newzbin.com/DTD/nzb/nzb-1.0.dtd">
          <nzb xmlns="http://www.newzbin.com/DTD/2003/nzb">
            <file poster="some poster@unknown.com" date="1298537493" subject="file subject">
              <groups>
                <group>alt.cool</group>
              </groups>
              <segments>
                <segment bytes="1234" number="1">abcd@segment.com</segment>
              </segments>
            </file>
           </nzb>""")

    def test_parser(self):
        """."""
        size, queue, skipped = parse_nzb(self.nzb)
        self.assertEqual(size, 1234)
        self.assertEqual(len(queue), 1)
        self.assertEqual(len(skipped), 0)

if __name__ == '__main__':
    unittest.main()
