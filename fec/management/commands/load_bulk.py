import csv
from datetime import datetime
from decimal import Decimal

from django.core.management.base import BaseCommand
from fec.models import Campaign, Committee, Contribution


class Command(BaseCommand):
    help = 'Imports FEC bulk data from https://www.fec.gov/data/browse-data/?tab=bulk-data'

    def add_arguments(self, parser):
        parser.add_argument('fec_type', type=str)
        parser.add_argument('bulk_file', type=str)

    def handle(self, *args, **options):
        fec_type = options['fec_type']
        filename = options['bulk_file']

        self.stdout.write("importing from '%s'" % filename)

        # try:
        record_creator = self._record_creator(fec_type)
        headers = self._lookup_headers(fec_type)

        with open(filename, newline='') as bulkfile:
            reader = csv.DictReader(
                bulkfile, headers, delimiter='|', quotechar='"')

            i = 0

            for row in reader:
                i += 1
                record_creator(row)
                print('.', end='', flush=True)

            print("loaded %d '%s' records" % (i, fec_type))
        # except Exception as exception:
        #     self.stderr.write(str(exception))

    def _record_creator(self, fec_type):
        if fec_type == "candidates":
            return self._save_candidate
        if fec_type == "committees":
            return self._save_committee
        if fec_type == "contributions":
            return self._save_contribution
        raise Exception("Invalid FEC type")

    def _save_candidate(self, row):
        record = Campaign(
            id=row['CAND_ID'],
            name=row['CAND_NAME'],
            office=row['CAND_OFFICE'],
            party=row['CAND_PTY_AFFILIATION'],
            state=row['CAND_ST'],
            district=row['CAND_OFFICE_DISTRICT'] or None)
        record.save()

    def _save_committee(self, row):
        campaign_id = row['CAND_ID']

        try:
            campaign = Campaign.objects.get(pk=campaign_id)
        except Campaign.DoesNotExist:
            campaign = None

        record = Committee(
            id=row['CMTE_ID'], name=row['CMTE_NM'], campaign=campaign)
        record.save()

    def _save_contribution(self, row):
        date = datetime.strptime(row['TRANSACTION_DT'], '%m%d%Y')
        amount = Decimal(row['TRANSACTION_AMT'])

        committee_id = row['CMTE_ID']
        committee = Committee.objects.get(pk=committee_id)

        record = Contribution(
            id=row['SUB_ID'],
            committee=committee,
            date=date,
            amount=amount,
            contributor_name=row['NAME'],
            contributor_city=row['CITY'],
            contributor_state=row['STATE'],
            contributor_zip=row['ZIP_CODE'],
            contributor_employer=row['EMPLOYER'],
            contributor_occupation=row['OCCUPATION'])
        record.save()

    def _lookup_headers(self, table):
        header_filename = "./fec/headers/%s.csv" % table

        with open(header_filename, newline='') as bulkfile:
            reader = csv.reader(bulkfile, delimiter=',')
            return next(reader)
