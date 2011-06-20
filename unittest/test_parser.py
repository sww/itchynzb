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
        """Test a regular parse."""
        size, queue, skipped = parse_nzb(self.nzb)
        self.assertEqual(size, 1234)
        self.assertEqual(len(queue), 1)
        self.assertEqual(len(skipped), 0)

    def test_parser_skip(self):
        """Tests the skip regex."""
        size, queue, skipped = parse_nzb('test.nzb', ['par2'])
        self.assertEqual(size, 8026)
        self.assertEqual(len(queue), 3)
        self.assertEqual(len(skipped), 1)
        self.assertEqual(skipped[0]['file_subject'], 'file subject 4.par2')

if __name__ == '__main__':
    unittest.main()
