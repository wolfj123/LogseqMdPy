import unittest
from my_python_library.logseq import name_to_filename, filename_to_name

class TestLogseqFunctions(unittest.TestCase):

    def test_name_to_filename(self):
        self.assertEqual(name_to_filename("test:name?"), "test%3Aname%3F")
        self.assertEqual(name_to_filename("example\"text\\"), "example%22text%2")
        self.assertEqual(name_to_filename("simple"), "simple")

    def test_filename_to_name(self):
        self.assertEqual(filename_to_name("test%3Aname%3F"), "test:name?")
        self.assertEqual(filename_to_name("example%22text%2"), "example\"text\\")
        self.assertEqual(filename_to_name("simple"), "simple")

if __name__ == '__main__':
    unittest.main()