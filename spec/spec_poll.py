from __future__ import annotations
import unittest


class TestPoll(unittest.TestCase):
    """
    Test the methods from `mel/poll.py`
    that don't require an external party.
    """

    def test_excuses_count(self) -> None:
        """
        Validate that the excuses count matches the expected row count.

        This test will prevent missing commas when adding excuses,
        causing two excuses to merge (uglily) into one.
        """

        from meldebot.mel.poll import MOTO_QUOTE

        assert len(MOTO_QUOTE) == 33
