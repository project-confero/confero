from django.test import TestCase

from .dummy import dummy


class DummyTests(TestCase):
    def tests_are_running(self):
        """
        Just a test of testing and code coverage. Remove this when we have real code.
        """
        self.assertIs(dummy(), 2)
