import unittest
from os import listdir, remove
from os.path import isfile, isdir, basename, dirname

from meldebot.mel import conf
import meldebot.mel.gif as melbot_gif


class TestConf(unittest.TestCase):
    def setUp(self):
        self.defaultname = "mortdegana.cfg"
        self.newfile = "mortdegana.mel"
        self.newpath = "mel/mortdegana.mel"
        # Ensure we don't commit the config file :S
        try:
            with open(self.defaultname, "r") as existing_file:
                raise Exception(
                    "Config file already exists!, Testing requires an empty environment"
                )
        except (IOError, FileNotFoundError):
            pass
        except:
            raise

    def tearDown(self):
        try:
            remove(self.defaultname)
        except (IOError, FileNotFoundError):
            pass
        try:
            remove(self.newfile)
        except (IOError, FileNotFoundError):
            pass
        try:
            remove(self.newpath)
        except (IOError, FileNotFoundError):
            pass

    def test_create_default_file(self):
        """Creation of a default config file"""
        # File does not exist before
        files = [f for f in listdir() if f == self.defaultname]
        self.assertFalse(self.defaultname in files)
        # Initialize config file
        conf.init_configs()
        # File must exist afterwards
        files = [f for f in listdir() if f == self.defaultname]
        self.assertTrue(self.defaultname in files)

    def test_create_with_path(self):
        """Creation of a default config file specifing the path"""
        # File does not exist before
        files = [f for f in listdir() if f == self.newfile]
        self.assertFalse(self.newfile in files)
        # Initialize config file
        conf.init_configs(self.newfile)
        # File must exist afterwards
        files = [f for f in listdir() if f == self.newfile]
        self.assertTrue(self.newfile in files)

    def test_create_with_new_path(self):
        """Creation of a default config file specifing a new path"""
        # Path does not exist before
        fname = basename(self.newpath)
        dname = dirname(self.newpath)
        # Initialize config file
        conf.init_configs(self.newpath)
        # File must exist afterwards
        self.assertTrue(isfile(self.newpath))

    def test_get_gif_provider_incorrect_provider(self):
        with self.assertRaises(SystemExit) as cm:
            melbot_gif.get_gif_provider("inventat")
        self.assertEqual(cm.exception.code, -1)

    def test_get_gif_provider_correct_provider(self):
        res = melbot_gif.get_gif_provider("giphy")
        self.assertEqual(res, melbot_gif.get_gif_url_giphy)

    def test_get_random_gif_provider(self):
        res = melbot_gif.get_random_gif_provider()
        self.assertIn(res, melbot_gif.GIF_PROVIDERS.values())
