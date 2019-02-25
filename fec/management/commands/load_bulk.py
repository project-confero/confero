import csv
from django.core.management.base import BaseCommand
from fec.models import Campaign


class Command(BaseCommand):
    help = 'Imports FEC bulk data from https://www.fec.gov/data/browse-data/?tab=bulk-data'

    def add_arguments(self, parser):
        parser.add_argument('fec_type', type=str)
        parser.add_argument('bulk_file', type=str)

    def handle(self, *args, **options):
        fec_type = options['fec_type']
        filename = options['bulk_file']

        self.stdout.write("importing from '%s'" % filename)

        try:
            record_creator = self._record_creator(fec_type)
            headers = self._lookup_headers(fec_type)

            with open(filename, newline='') as bulkfile:
                reader = csv.DictReader(
                    bulkfile, headers, delimiter='|', quotechar='"')

                for row in reader:
                    record_creator(row)
        except Exception as exception:
            self.stderr.write(str(exception))

    def _record_creator(self, fec_type):
        if fec_type == "candidates":
            return self._save_candidate
        if fec_type == "committees":
            return self._save_committee
        raise Exception("Invalid FEC type")

    def _save_candidate(self, row):
        record = Campaign(
            id=row['CAND_ID'],
            name=row['CAND_NAME'],
            office=row['CAND_OFFICE'],
            party=row['CAND_PTY_AFFILIATION'],
            state=row['CAND_ST'],
            district=row['CAND_OFFICE_DISTRICT'])
        record.save()

    def _save_committee(self, row):
        record = Campaign(
            id=row['CAND_ID'],
            name=row['CAND_NAME'],
            office=row['CAND_OFFICE'],
            party=row['CAND_PTY_AFFILIATION'],
            state=row['CAND_ST'],
            district=row['CAND_OFFICE_DISTRICT'])
        record.save()

    def _lookup_headers(self, table):
        header_filename = "./fec/headers/%s.csv" % table

        with open(header_filename, newline='') as bulkfile:
            reader = csv.reader(bulkfile, delimiter=',')
            return next(reader)
