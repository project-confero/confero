from django.test import TestCase

from .models import Campaign


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
