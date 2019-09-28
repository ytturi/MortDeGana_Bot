import unittest
from os import listdir, remove

from meldebot import confs

class TestConfs(unittest.TestCase):
    def setUp(self):
        self.fname = 'mortdegana.cfg'
        try:
            with open(self.fname, 'r') as existing_file:
                raise Exception('Config file already exists!, Testing requires an empty environment')
        except (IOError, FileNotFoundError):
            pass
        except:
            raise

    def tearDown(self):
        try:
            remove(self.fname)
        except (IOError, FileNotFoundError):
            pass

    def test_create_default_file(self):
        files = [f for f in listdir() if f==self.fname]
        self.assertFalse(self.fname in files)
        confs.init_configs()
        files = [f for f in listdir() if f==self.fname]
        self.assertTrue(self.fname in files)

    def test_create_with_path(self):
        self.skipTest('TODO')

    def test_create_with_args(self):
        self.skipTest('TODO')
