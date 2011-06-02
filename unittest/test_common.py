import unittest
import common.helper as helper
#import common.compressed as compressed

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
            ("""Blank""", None)
        ]

        for subject, expected_filename in test_subjects:
            filename = helper.get_filename_from(subject)
            self.assertEqual(filename, expected_filename)

    # def test_get_nzb_file(self):
    #     nzb_files = helper.get_nzb_file('testfiles')
    #     self.assertEqual(['testfiles/at.nzb'], nzb_files)

    #     nzb_files = helper.get_nzb_file('testfiles/at.nzb')
    #     self.assertEqual(['testfiles/at.nzb'], nzb_files)

    #     nzb_files = helper.get_nzb_file('')
    #     self.assertEqual([''], nzb_files)
 
# class TestCompressedFunctions(unittest.TestCase):
#     def setUp(self):
#         pass

#     def test_unzip(self):
#         nzb_list = compressed.unzip('testfiles/foo.zip')

#         self.assertEqual(2, len(nzb_list))
        
#         contains = 'testfiles/Professor_Layton_and_the_Unwound_Future_NDS-VENOM.nzb' in nzb_list
#         self.assertTrue(contains)

#         contains = 'testfiles/Professor_Layton_and_the_Unwound_Future_USA_CLEAN_NDS-NukeThis.nzb' in nzb_list

#         self.assertTrue(contains)

#         contains = 'not_a_nzb_file' in nzb_list
        
#         self.assertFalse(contains)
        
#     def tearDown(self):
#         from os import remove

#         remove('testfiles/Professor_Layton_and_the_Unwound_Future_USA_CLEAN_NDS-NukeThis.nzb')
#         remove('testfiles/Professor_Layton_and_the_Unwound_Future_NDS-VENOM.nzb')
    
if __name__ == '__main__':
    unittest.main()
