import StringIO
import unittest
from yenc import yenc_decode

class TestYenc(unittest.TestCase):
    def setUp(self):
        # Normal case: single part.
        self.yenc = StringIO.StringIO("""=ybegin\n""")
        # Normal case: multiple parts.
        self.yenc_part = StringIO.StringIO()
        # Lots of newline space at the beginning and end.
        self.yenc_fun = StringIO.StringIO("""\n\n\n=ybegin""")

    def test_yenc_decode(self):
        yenc_decode()

if __name__ == '__main__':
    unittest.main()
