import factory
import factory.fuzzy
from fec.models import Candidate, Committee, Contribution, Connection


class CandidateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Candidate

    id = factory.Faker('uuid4')
    name = factory.Faker('first_name')
    state = factory.Faker('state_abbr')
    district = factory.Faker('pyint')

    office = factory.fuzzy.FuzzyChoice(
        [Candidate.HOUSE, Candidate.SENATE, Candidate.PRESIDENT])

    party = factory.fuzzy.FuzzyChoice(Candidate.PARTIES)


class CommitteeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Committee

    id = factory.Faker('ean8')
    name = factory.Faker('company')


class ContributionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contribution

    id = factory.Faker('pyint')
    amount = factory.Faker('pyint')
    date = factory.Faker(
        'date_this_year',
        before_today=True,
        after_today=False,
    )


class ConnectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Connection

    score = factory.Faker('pyint')
