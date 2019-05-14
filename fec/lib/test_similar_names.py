import re
from unittest import TestCase
from fec.lib.similar_names import regex_name


class SimilarNamesTest(TestCase):
    def setUp(self):
        self.nickname = 'SMITH, JUDY MD.'
        self.regex = re.compile(regex_name(self.nickname))

    def test_nickname_matches_given(self):
        self.assertIsNotNone(self.regex.match('SMITH MD., JUDITH R'))

    def test_nickname_matches_short(self):
        self.assertIsNotNone(self.regex.match('SMITH, JUDY'))

    def test_nickname_matches_nickname(self):
        self.assertIsNotNone(self.regex.match(self.nickname))

    def test_unmatching_name(self):
        self.assertIsNone(self.regex.match('SMITH, JOHN'))
