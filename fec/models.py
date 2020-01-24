from django.db import models
from django.db.models import Q

# The minimum score that counts as a valid connection. Filters out one-off connections.
MIN_SCORE = 2


class Candidate(models.Model):
    HOUSE = 'H'
    SENATE = 'S'
    PRESIDENT = 'P'

    OFFICE_CHOICES = (
        (HOUSE, 'House'),
        (SENATE, 'Senate'),
        (PRESIDENT, 'President'),
    )

    PARTIES = {'DEM': 'Democrat', 'REP': 'Repbulican'}

    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=200)
    office = models.CharField(max_length=1, choices=OFFICE_CHOICES, null=True)
    party = models.CharField(max_length=3, null=True)
    state = models.CharField(max_length=2, null=True)
    district = models.IntegerField(blank=True, null=True)

    def party_abbreviation(self):
        return self.party[0]

    def party_full(self):
        return self.PARTIES.get(self.party, self.party)

    def similar_candidates(self):
        connections = self.source_connections.order_by(
            "-score").select_related("target")[:10]

        candidates = []
        for connection in connections:
            target = connection.target
            target.contributor_count = connection.score
            candidates.append(target)

        return candidates

    @staticmethod
    def connected_candidates():
        return Candidate.objects.filter(
            source_connections__score__gte=MIN_SCORE).distinct()

    @staticmethod
    def search(data):
        """Search by name, id, or comittee id."""

        return Candidate.objects.filter(Q(id=data) | Q(name__icontains=data))


class Committee(models.Model):
    committee_id = models.CharField(max_length=9, primary_key=True)

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        # Allow mis-matched data
        db_constraint=False,
    )


class Contribution(models.Model):
    id = models.BigIntegerField(primary_key=True)  # FEC SUB_ID

    committee = models.ForeignKey(
        Committee,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        # Allow mis-matched data
        db_constraint=False,
    )
    name = models.CharField(max_length=200, null=True)
    zip = models.CharField(max_length=9, null=True)
    employer = models.CharField(max_length=38, null=True)
    occupation = models.CharField(max_length=38, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name', 'zip', 'employer', 'occupation'])
        ]


class Connection(models.Model):
    source = models.ForeignKey(
        Candidate,
        on_delete=models.PROTECT,
        related_name='source_connections',
    )
    target = models.ForeignKey(
        Candidate,
        on_delete=models.PROTECT,
        related_name='target_connections',
    )
    score = models.IntegerField()

    def to_edge(self):
        return {
            "target": self.target_id,
            "source": self.source_id,
            "score": self.score,
        }

    @staticmethod
    def edges():
        connections = Connection.objects.filter(score__gte=MIN_SCORE).all()
        m = map(lambda connection: connection.to_edge(), connections)
        return list(m)
