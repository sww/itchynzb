import os
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
            ("""[65781]-[FULL]-[#a.b.test@EFNet]-[ Legit.File.MEDiA-GROUP ]-[25/29] - &quot;a.real.file.vol01+02.par2&quot;""", 'a.real.file.vol01+02.par2'),
            ("""[65781]-[FULL]-[#a.b.test@EFNet]-[ Legit.File.MEDiA-GROUP ]-[25/29] - a.real.file.vol01+02.par2 blah""", 'a.real.file.vol01+02.par2'), # Should test the second regex.
            ("""Just a file.jpg""", "Just a file.jpg"),
            ("""filename.jpg""", "filename.jpg"),
            ("""Blank""", '')
        ]

        for subject, expected_filename in test_subjects:
            potential = helper.get_filename_from(subject)
            try:
                self.assertTrue(expected_filename in potential)
            except AssertionError:
                print '* failed on subject', repr(subject)
                print '* got', repr(potential)
                print '* expected', repr(expected_filename)
                raise

    def test_htime(self):
        self.assertEqual(helper.htime(1234), '20m 34s')
        self.assertEqual(helper.htime(53), '53s')
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
        cwd = os.getcwd()
        nzb_dir = 'files/nzb'
        settings_dir = 'files/settings'

        self.assertEqual(helper.get_nzb_file(os.path.join(cwd, nzb_dir)),
                         [os.path.join(cwd, nzb_dir, nzb) for nzb in ['broken.nzb', 'gpl.nzb', 'gutenberg.nzb']])
        self.assertEqual(helper.get_nzb_file(os.path.join(cwd, settings_dir)), [])

        # Test a zip file.
        self.assertEqual(helper.get_nzb_file(os.path.join(cwd, nzb_dir, 'nzbs.zip')), [os.path.join(cwd, nzb_dir, nzb) for nzb in ['gpl.nzb', 'gutenberg.nzb']])

        # OptionParser's args come in a list, so emulate that.
        self.assertEqual(helper.get_nzb_file([os.path.join(cwd, nzb_dir, 'nzbs.zip')]), [os.path.join(cwd, nzb_dir, nzb) for nzb in ['gpl.nzb', 'gutenberg.nzb']])

    def test_get_download_path(self):
        self.assertEqual(helper.get_download_path('', 'test.nzb'), 'test')
        self.assertEqual(helper.get_download_path('dir/', 'test.nzb'), 'dir/test')

    def test_file_exists(self):
        self.assertTrue(helper.file_exists('.', 'test_common.py'))
        self.assertFalse(helper.file_exists('.', 'nosuch file'))

    def tearDown(self):
        pass
   
if __name__ == '__main__':
    unittest.main()
