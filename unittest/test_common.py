import os
import tempfile
import unittest
import common.helper as helper

class TestCommonFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_filename_from(self):
        # Subject, expected filename.
        test_subjects = [
            ("""I AM A LAME SUBJECT "FILENAME.POOP" HA""", 'FILENAME.POOP'),
            ("""I AM A LAME SUBJECT "FILE.NAME.POOP" HA""", 'FILE.NAME.POOP'),
            ("""[123456]-[01/21] - &quot;0_0.nfo&quot; yEnc (1/1)""", '0_0.nfo'),
            ("""[123456]-[#chan@irc]-[Full]-[Title_of_the-Relase-GROuP]-[01/21] - this_is_the_filename.nfo yEnc (1/1)""", 'this_is_the_filename.nfo'),
            ("""[123456]-[#chan@irc]-[Full]-[Title_of_the-Relase-GROuP]-[01/21] - this is the filename.nfo yEnc (1/1)""", 'this is the filename.nfo'),
            ("""this_is_the_filename.nfo""", 'this_is_the_filename.nfo'),
            ("""this is the filename.nfo""", 'this is the filename.nfo'),
            ("""[1235]-[#chan@IrC]-[FULL]-[12345]-[21/79] - some.file.r01 (1/50)""", 'some.file.r01'),
            ("""[353]-[#chan@IrC]-[FULL]-[10202]-[21/79] - "some.file.r01" (1/50)""", 'some.file.r01'),
            ("""New subject name "Filename goes here (v5.0) (echo).rar" (1/3)""", 'Filename goes here (v5.0) (echo).rar'),
            ("""Blank""", '')
        ]

        for subject, expected_filename in test_subjects:
            filename = helper.get_filename_from(subject)
            try:
                self.assertEqual(filename, expected_filename)
            except:
                print subject
                raise

    def test_htime(self):
        self.assertEqual(helper.htime(1234), '20m 34s')
        self.assertEqual(helper.htime(53), '0m 53s')
        self.assertEqual(helper.htime(3720), '1h 2m 0s')

    def test_get_size(self):
        self.assertEqual(helper.get_size(1000), '0.98 KB')
        self.assertEqual(helper.get_size(25600), '25.0 KB')
        self.assertEqual(helper.get_size(1024*1024*3), '3.0 MB')
        self.assertEqual(helper.get_size(1024**3*2.3), '2.3 GB')
        self.assertEqual(helper.get_size(1024**4*5.5), '5.5 TB')
        self.assertEqual(helper.get_size(1234, True), 'KB')
        self.assertEqual(helper.get_size(1024*1024*32, True), 'MB')
        self.assertEqual(helper.get_size(1024**3*77, True), 'GB')
        self.assertEqual(helper.get_size(1024**4*1.2, True), 'TB')
        self.assertEqual(helper.get_size(0), '0.00 KB')

    def test_get_nzb_file(self):
        self.assertEqual(helper.get_nzb_file('.'), ['./gpl.nzb', './test.nzb'])
        tempdir = tempfile.mkdtemp()
        self.assertEqual(helper.get_nzb_file(tempdir), [])
        os.rmdir(tempdir)

    def test_get_download_path(self):
        self.assertEqual(helper.get_download_path('', 'test.nzb'), 'test')
        self.assertEqual(helper.get_download_path('dir/', 'test.nzb'), 'dir/test')
   
if __name__ == '__main__':
    unittest.main()
