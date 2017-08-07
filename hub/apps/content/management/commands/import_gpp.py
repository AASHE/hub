import csv
from django.core.management.base import BaseCommand, CommandError

from hub.apps.content.models import GreenPowerProject
from hub.apps.metadata.models import Organization


class Command(BaseCommand):
    help = "One-time import of Green Power Project data"

    def handle(self, *args, **options):

        install_types = dict([(i[1], i[0]) for i in GreenPowerProject.INSTALLATION_TYPES])
        ownership_types = dict([(o[1], o[0]) for o in GreenPowerProject.OWNERSHIP_TYPES])

        with open('/tmp/gpp.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            row = reader.next()
            print row.keys()
            for row in reader:

                install_type1 = row['Installation Type 1']
                install_type2 = row['Installation Type 2']
                install_type3 = row['Installation Type 3']

                new_gpp = GreenPowerProject(
                    title=row['Project Name'],
                    description=row['Project Overview'],
                    project_size=int(row['Project Size (kW)'].replace(',', '')),
                    annual_production=int(row['Approximate Annual Production (kWh)'].replace(',', '')),
                    installed_cost=int(row['Installed Cost (U.S. Dollars)'].replace(',', '').replace('$', '')),
                    first_installation_type=install_types[install_type1],
                    ownership_type=ownership_types[row['Ownership type']]
                )

                if install_type2:
                    new_gpp.second_installation_type = install_types[install_type2]
                if install_type3:
                    new_gpp.third_installation_type = install_types[install_type3]

                new_gpp.save()

                #get orgs
                # up to 4 orgs
                for idx in (1, 2, 3, 4):
                    org_id = row['Organization{}_ID'.format(idx)]
                    if org_id:
                        org = Organization.objects.get(account_num=org_id)
                        new_gpp.organizations.add(org)





                #parse and create Tags


                #TODO date installed?


