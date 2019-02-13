from django.db import models


class Politician(models.Model):
    name = models.CharField(max_length=200)


class Campaign(models.Model):
    HOUSE = 'H'
    SENATE = 'S'
    PRESIDENT = 'P'

    OFFICE_CHOICES = ((HOUSE, 'House'), (SENATE, 'Senate'), (PRESIDENT,
                                                             'President'))

    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    politician = models.ForeignKey(Politician, on_delete=models.CASCADE)
    office = models.CharField(max_length=1, choices=OFFICE_CHOICES)
    party = models.CharField(max_length=3)
    state = models.CharField(max_length=2)
    district = models.IntegerField()
