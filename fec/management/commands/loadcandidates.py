from django.core.management.base import BaseCommand
import csv
from fec.models import Campaign

# TODO: Import data
# Open file:
# Parse CSV: https://docs.python.org/3.7/library/csv.html


class Command(BaseCommand):
    help = 'Imports bulk data from Cadidate Master at: https://www.fec.gov/data/browse-data/?tab=bulk-data'

    def add_arguments(self, parser):
        parser.add_argument('bulk_file', type=str)

    def handle(self, *args, **options):
        self.stdout.write('importing from ' + options['bulk_file'])

        with open(options['bulk_file'], newline='') as bulkfile:
            reader = csv.reader(bulkfile, delimiter=',', quotechar='"')
            for row in reader:
              # create Campaign
