import csv
from django.core.management.base import BaseCommand, CommandError

from hub.apps.content.models import GreenPowerProject


class Command(BaseCommand):
    help = "One-time import of Green Power Project data"

    def handle(self, *args, **options):
        pass


    with open('/tmp/gpp.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        row = reader.next()
        print row.keys()
        for row in reader:
            new_gpp = GreenPowerProject(
                title=row['Project Name'],
                description=row['Project Overview'],
                project_size=row['Project Size (kW)'],
                annual_production=row['Approximate Annual Production (kWh)'],
                installed_cost=row['Installed Cost (U.S. Dollars)']
            )

            #get orgs
            # Organization1_ID
            # up to 4 orgs


            #parse and create Tags


            #TODO date installed?


