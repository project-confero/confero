from django.db import models
from django.db.models import Q


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

    @staticmethod
    def search(data):
        """Search by name, id, or comittee id."""

        # Note the distinct(), because the many-to-many committee__id
        # check returns duplicates.
        return Campaign.objects.filter(
            Q(id=data) | Q(name__icontains=data)
            | Q(committee__id=data)).distinct()


class Committee(models.Model):
    id = models.CharField(max_length=9, primary_key=True)

    campaign = models.ForeignKey(
        Campaign, on_delete=models.PROTECT, blank=True, null=True)

    name = models.CharField(max_length=200)


class Contributor(models.Model):
    contributor_name = models.CharField(max_length=200)
    contributor_city = models.CharField(max_length=30)
    contributor_state = models.CharField(max_length=2)
    contributor_zip = models.CharField(max_length=9)
    contributor_employer = models.CharField(max_length=38)
    contributor_occupation = models.CharField(max_length=38)

    f = [
        '.',
        ' DR',
        ' SR',
        ' JR',
        ' II',
        ' III',
        ' IV',
        ' MD',
        ' MR',
        ' MRS',
        ' MS',
    ]

    def first_names(self):

        return self.fixes(self.contributor_name.split(',')[1]).split()

    def last_name(self):

        return self.fixes(self.contributor_name.split(',')[0])

    def fixes(self, string_to_fix):

        for fix in self.f:
            string_to_fix = string_to_fix.replace(fix, '')

        return string_to_fix

    def get_nicknames(self, name):
        """Returns regex string for a common name"""

        # Make 2 data structures - "lines" is a dictionary with given name as key,
        # and "names" which is all names as a list of lists with name and index number
        names, lines = self.get_names_data('./fec/data/names.txt')

        # Search for all names that match first_name
        all_names = self.nickname_search(name, names)

        if all_names is None:
            return [name]

        names = [
            lines[all_names[index][1]][0] for index, _ in enumerate(all_names)
        ]
        return names

    @staticmethod
    def get_names_data(file_path):
        lines = []
        with open(file_path) as file:
            for index, line in enumerate(file.readlines()):
                lines.append(line.strip('\n').split(','))
                names = [[name, index] for name in line.split(',')]
                names.sort()
            names.sort()
            return names, lines

    @staticmethod
    def nickname_search(first_name, names):
        """ Find and return the index of key in sequence names """
        lb = 0
        ub = len(names)

        while True:
            if lb == ub:  # If region of interest (ROI) becomes empty
                return None
            # Next probe should be in the middle of the ROI
            mid_index = (lb + ub) // 2
            # Fetch the item at that position
            item_at_mid = names[mid_index][0]
            # How does the probed item compare to the target?
            if item_at_mid == first_name:
                upper_mid_index = mid_index
                lower_mid_index = mid_index
                while names[upper_mid_index + 1][0] == first_name:
                    upper_mid_index = upper_mid_index + 1
                while names[lower_mid_index - 1][0] == first_name:
                    lower_mid_index = lower_mid_index - 1
                return names[lower_mid_index:upper_mid_index + 1]  # Found it!
            if item_at_mid < first_name:
                lb = mid_index + 1  # Use upper half of ROI next time
            else:
                ub = mid_index  # Use lower half of ROI next time

    def regex_name(self):

        regex_fixes = '({0})?'.format('|'.join([f + '(.)?' for f in self.f]))
        first_name, *rest_of_first = self.first_names()
        try:
            return regex_fixes + self.last_name() + regex_fixes + \
                ', ({0})'.format('|'.join(self.get_nicknames(first_name))) + \
                '({0})?'.format('|'.join(rest_of_first)) + regex_fixes
        except IndexError:
            return self.contributor_name

    @staticmethod
    def search(contributor):
        return Contributor.objects.\
            filter(
                Q(contributor_name__regex=contributor.regex_name())
                & Q(contributor_zip=contributor.contributor_zip))


class Contribution(models.Model):
    id = models.BigIntegerField(primary_key=True)  # FEC SUB_ID

    contributor = models.ForeignKey(
        Contributor, on_delete=models.PROTECT, blank=True, null=True)
    committee = models.ForeignKey(
        Committee, on_delete=models.PROTECT, blank=True, null=True)  # CMTE_ID
    date = models.DateField()
    amount = models.DecimalField(max_digits=16, decimal_places=2)

    @staticmethod
    def for_campaign(campaign):
        """Get all contributions to a Campaign"""

        return Contribution.objects.filter(committee__campaign=campaign)
