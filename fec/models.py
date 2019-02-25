from django.db import models


class Campaign(models.Model):
    HOUSE = 'H'
    SENATE = 'S'
    PRESIDENT = 'P'

    OFFICE_CHOICES = ((HOUSE, 'House'), (SENATE, 'Senate'), (PRESIDENT,
                                                             'President'))

    PARTIES = {'DEM': 'Democrat', 'REP': 'Repbulican'}

    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    office = models.CharField(max_length=1, choices=OFFICE_CHOICES)
    party = models.CharField(max_length=3)
    state = models.CharField(max_length=2)
    district = models.IntegerField(blank=True, null=True)

    def party_abbreviation(self):
        return self.party[0]

    def party_full(self):
        return self.PARTIES.get(self.party, self.party)


class Committee(models.Model):
    id = models.CharField(max_length=9, primary_key=True)

    campaign = models.ForeignKey(
        Campaign, on_delete=models.PROTECT, blank=True, null=True)

    name = models.CharField(max_length=200)


class Contribution(models.Model):
    id = models.BigIntegerField(primary_key=True)  # FEC SUB_ID

    committee = models.ForeignKey(
        Committee, on_delete=models.PROTECT, blank=True, null=True)  # CMTE_ID
    date = models.DateField()
    amount = models.DecimalField(max_digits=16, decimal_places=2)

    contributor_name = models.CharField(max_length=200)
    contributor_city = models.CharField(max_length=30)
    contributor_state = models.CharField(max_length=2)
    contributor_zip = models.CharField(max_length=9)
    contributor_employer = models.CharField(max_length=38)
    contributor_occupation = models.CharField(max_length=38)
