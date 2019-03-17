from django.test import TestCase

from .models import Campaign, Contributor


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
        self.givenname = Contributor(
            contributor_name='SMITH MD., JUDITH R',
            contributor_city='Manchester',
            contributor_state='NH',
            contributor_zip='03104',
            contributor_employer='Self',
            contributor_occupation='PHYSICIAN')

        self.assertEqual(self.nickname.id,
                         Contributor.search(self.givenname)[0].id)

    def test_nickname_matches_short(self):
        self.short = Contributor(
            contributor_name='SMITH, JUDY',
            contributor_city='Manchester',
            contributor_state='NH',
            contributor_zip='03104',
            contributor_employer='Self',
            contributor_occupation='PHYSICIAN')
        self.assertEqual(self.nickname.id,
                         Contributor.search(self.short)[0].id)

    def test_nickname_matches_nickname(self):
        self.nickname2 = Contributor(
            contributor_name='SMITH, JUDY MD.',
            contributor_city='Manchester',
            contributor_state='NH',
            contributor_zip='03104',
            contributor_employer='Self',
            contributor_occupation='PHYSICIAN')
        self.assertEqual(self.nickname.id,
                         Contributor.search(self.nickname2)[0].id)
