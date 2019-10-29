from django.test import TestCase

from .models import Candidate
from .factories import CandidateFactory, ConnectionFactory


class CandidateTests(TestCase):
    def setUp(self):
        self.candidate = Candidate.objects.create(
            id="abc123",
            name="Bob 4 Prez",
            office="P",
            party="DEM",
        )

    def test_create_candidates(self):
        candidate = Candidate.objects.get(pk=self.candidate.id)

        self.assertEqual(candidate.name, "Bob 4 Prez")

    def test_party_abbreviation(self):
        self.assertEqual(self.candidate.party_abbreviation(), "D")

    def test_full_party(self):
        self.assertEqual(self.candidate.party_abbreviation(), "D")

    def test_search_empty(self):
        candidates = Candidate.search("Nobody")
        assert not candidates

    def test_search_by_name(self):
        candidates = Candidate.search("Bob")

        self.assertEqual(candidates[0], self.candidate)

    def test_search_by_id(self):
        candidates = Candidate.search(self.candidate.id)

        self.assertEqual(candidates[0], self.candidate)

    def test_similar_candidates(self):
        alice = CandidateFactory.create(name="Alice")
        alex = CandidateFactory.create(name="Alex")
        bob = CandidateFactory.create(name="Bob")

        ConnectionFactory.create(source=alice, target=bob, score=1)
        ConnectionFactory.create(source=alice, target=alex, score=2)

        similar_candidates = alice.similar_candidates()

        self.assertEqual(similar_candidates[0].name, alex.name)
        self.assertEqual(similar_candidates[1].name, bob.name)

        self.assertEqual(similar_candidates[0].contributor_count, 2)
        self.assertEqual(similar_candidates[1].contributor_count, 1)

