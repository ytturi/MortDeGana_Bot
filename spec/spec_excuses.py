from __future__ import annotations

import unittest

from meldebot.mel.excuses import EXCUSES, get_random_excuse


class TestExcuses(unittest.TestCase):
    """
    Test the methods from `mel/excuses.py`
    that don't require an external party.
    """

    def test_excuses_count(self) -> None:
        """
        Validate that the excuses count matches the expected row count.

        This test will prevent missing commas when adding excuses,
        causing two excuses to merge (uglily) into one.
        """
        assert len(EXCUSES) == 63

    def test_get_random_excuses_function(self) -> None:
        """
        Validate that the get_random_excuses returns a str.

        This test will check get_random_excuses executes its purpose correctly,
        choosing and returning one of the excuses defined by users.
        """
        assert isinstance(get_random_excuse(), str)
