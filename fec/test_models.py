from django.test import TestCase

from .models import Campaign, Contributor
from .factories import CampaignFactory, ContributorFactory, CommitteeFactory, ContributionFactory


class CampaignTests(TestCase):
    def setUp(self):
        self.campaign = Campaign.objects.create(
            id="abc123", name="Bob 4 Prez", office="P", party="DEM")

    def test_create_campaigns(self):
        campaign = Campaign.objects.get(pk=self.campaign.id)

        self.assertEqual(campaign.name, "Bob 4 Prez")

    def test_party_abbreviation(self):
        self.assertEqual(self.campaign.party_abbreviation(), "D")

    def test_full_party(self):
        self.assertEqual(self.campaign.party_abbreviation(), "D")

    def test_search_empty(self):
        campaigns = Campaign.search("Nobody")
        assert not campaigns

    def test_search_by_name(self):
        campaigns = Campaign.search("Bob")

        self.assertEqual(campaigns[0], self.campaign)

    def test_search_by_id(self):
        campaigns = Campaign.search(self.campaign.id)

        self.assertEqual(campaigns[0], self.campaign)

    def test_similar_campaigns(self):
        alice = CampaignFactory.create(name="Alice")
        alex = CampaignFactory.create(name="Alex")
        bob = CampaignFactory.create(name="Bob")

        alice_committee = CommitteeFactory.create(
            name="alice 4 prez", campaign=alice)
        alex_committee = CommitteeFactory.create(
            name="alex 4 prez", campaign=alex)
        bob_committee = CommitteeFactory.create(
            name="bob 4 prez", campaign=bob)

        a_contributor_1 = ContributorFactory.create()
        a_contributor_2 = ContributorFactory.create()
        b_contributor_1 = ContributorFactory.create()
        b_contributor_2 = ContributorFactory.create()
        anti_alex_contributor = ContributorFactory.create()

        ContributionFactory.create(
            committee=alice_committee, contributor=a_contributor_1)

        ContributionFactory.create(
            committee=alex_committee, contributor=a_contributor_1)

        ContributionFactory.create(
            committee=alice_committee, contributor=a_contributor_2)

        ContributionFactory.create(
            committee=alex_committee, contributor=a_contributor_2)

        ContributionFactory.create(
            committee=bob_committee, contributor=b_contributor_1)

        ContributionFactory.create(
            committee=bob_committee, contributor=b_contributor_2)

        ContributionFactory.create(
            committee=alice_committee, contributor=anti_alex_contributor)

        ContributionFactory.create(
            committee=bob_committee, contributor=anti_alex_contributor)

        alice_committee.refresh_from_db()
        similar_campaigns = alice.similar_campaigns()

        self.assertEqual(similar_campaigns[0].name, alex.name)
        self.assertEqual(similar_campaigns[1].name, bob.name)

        self.assertEqual(similar_campaigns[0].contributor_count, 2)
        self.assertEqual(similar_campaigns[1].contributor_count, 1)


class ContributersTest(TestCase):
    def setUp(self):
        self.nickname = Contributor.objects.create(
            contributor_name='SMITH, JUDY MD.',
            contributor_city='Manchester',
            contributor_state='NH',
            contributor_zip='03104',
            contributor_employer='Self',
            contributor_occupation='PHYSICIAN')

    def test_nickname_matches_given(self):
        givenname = Contributor(
            contributor_name='SMITH MD., JUDITH R',
            contributor_city='Manchester',
            contributor_state='NH',
            contributor_zip='03104',
            contributor_employer='Self',
            contributor_occupation='PHYSICIAN')
        self.assertEqual(self.nickname.id, Contributor.search(givenname)[0].id)

    def test_nickname_matches_short(self):
        short = Contributor(
            contributor_name='SMITH, JUDY',
            contributor_city='Manchester',
            contributor_state='NH',
            contributor_zip='03104',
            contributor_employer='Self',
            contributor_occupation='PHYSICIAN')
        self.assertEqual(self.nickname.id, Contributor.search(short)[0].id)

    def test_nickname_matches_nickname(self):
        nickname2 = Contributor(
            contributor_name='SMITH, JUDY MD.',
            contributor_city='Manchester',
            contributor_state='NH',
            contributor_zip='03104',
            contributor_employer='Self',
            contributor_occupation='PHYSICIAN')
        self.assertEqual(self.nickname.id, Contributor.search(nickname2)[0].id)
