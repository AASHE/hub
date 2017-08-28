import csv
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from hub.apps.content.models import GreenPowerProject, Website
from hub.apps.metadata.models import Organization


User = get_user_model()


class Command(BaseCommand):
    help = "One-time import of Green Power Project data; Use the import_gpp settings"

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
                cost = row['Installed Cost (U.S. Dollars)'].replace(',', '').replace('$', '')
                if cost:
                    cost = int(cost)
                else:
                    cost = None
                annual_prod = row['Approximate Annual Production (kWh)'].replace(',', '')
                if annual_prod:
                    annual_prod = int(annual_prod)
                else:
                    annual_prod = None

                _d = [int(p) for p in row['Date Posted'].split('/')]
                date_posted = datetime(_d[2], _d[0], _d[1])
                _d = [int(p) for p in row['Date Installed'].split('/')]
                date_installed = datetime(_d[2], _d[0], _d[1])

                new_gpp = GreenPowerProject(
                    title=row['Project Name'],
                    description=row['Project Overview'],
                    project_size=int(row['Project Size (kW)'].replace(',', '')),
                    annual_production=annual_prod,
                    installed_cost=cost,
                    first_installation_type=install_types[install_type1],
                    ownership_type=ownership_types[row['Ownership type']],
                    date_created=date_posted,
                    date_installed=date_installed
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
                tags_token = row['Tag(s)']
                tags = [tag.strip() for tag in tags_token.split(',')]
                new_gpp.tags = tags
                new_gpp.save()


                # project contact

                # uploads

                # urls
                for i in range(1, 6):
                    url = row['URL{}'.format(i)]
                    if url:
                        Website.objects.create(
                            url=url,
                            ct=new_gpp
                        )

                # submitter
                submitter_email = row['Submitter email']
                try:
                    # TODO Handle submitter doesn't exist
                    submitter_user = User.objects.get(email=submitter_email)
                    new_gpp.submitted_by = submitter_user
                    new_gpp.save()
                except User.DoesNotExist:
                    print 'Submitter not found ', submitter_email
