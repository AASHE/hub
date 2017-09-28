import os.path
import csv
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from hub.apps.content.models import GreenPowerProject, Website, Author
from hub.apps.metadata.models import Organization, SustainabilityTopic, GreenPowerInstallation, GreenPowerLocation, \
    GreenPowerFinanceOption
from hub.imports.utils import create_file_from_url


User = get_user_model()


class Command(BaseCommand):
    help = "One-time import of Green Power Project data; Use the import_gpp settings"

    def handle(self, *args, **options):

        INSTALLATION_TYPES = (
            ('solar-canopy', 'Solar - Canopy'),
            ('solar-rooftop', 'Solar - Roof Top Mount'),
            ('solar-wall', 'Solar - Wall Mount'),
            ('solar-ground-pole', 'Solar - Ground or Pole Mount'),
            ('solar-building-photovoltaic', 'Solar - Building Integrated Photovoltaic'),
            ('solar-other', 'Solar - Other'),
            ('wind-horizontal', 'Wind - Horizontal Axis'),
            ('wind-horizontal', 'Wind - Vertical Axis'),
            ('hydroelectric', 'Low Impact Hydroelectric'),
        )

        # Create Installation choices
        installation_types = {}
        for _, name in INSTALLATION_TYPES:
            installation_types[name] = GreenPowerInstallation.objects.create(name=name)

        FINANCE_TYPES = (
            ('operating-budget', 'Operating budget'),
            ('endowment', 'Endowment'),
            ('capital-budget', 'Capital budget'),
            ('third-party', 'Third party'),
            ('donation', 'Donation'),
        )

        finance_types = {}
        for _, name in FINANCE_TYPES:
            finance_types[name] = GreenPowerFinanceOption.objects.create(name=name)

        ownership_types = dict([(o[1], o[0]) for o in GreenPowerProject.OWNERSHIP_TYPES])

        LOCATION_CHOICES = (
            ('institution-owned-main', 'Institution-owned property (main campus)'),
            ('institution-owned-remote', 'Institution-owned property (remote)'),
            ('Third party-owned', 'Third party-owned property'),
            ('unknown', 'Unknown'),
        )

        location_options = {}
        for _, name in LOCATION_CHOICES:
            location_options[name] = GreenPowerLocation.objects.create(name=name)

        user_monika = User.objects.get(email='monika.urbanski@aashe.org')
        energy_topic = SustainabilityTopic.objects.get(slug='energy')

        with open("{}/{}".format(os.path.dirname(__file__), 'green_power_projects.csv'), 'rb') as csvfile:
            reader = csv.DictReader(csvfile)

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
                date_submitted = timezone.datetime(_d[2], _d[0], _d[1])
                _d = [int(p) for p in row['Date Installed'].split('/')]
                date_installed = datetime(_d[2], _d[0], _d[1])

                new_gpp = GreenPowerProject(
                    title=row['Project Name'],
                    description=row['Project Overview'],
                    project_size=int(row['Project Size (kW)'].replace(',', '')),
                    annual_production=annual_prod,
                    installed_cost=cost,
                    ownership_type=ownership_types[row['Ownership type']],
                    date_created=date_installed,
                    date_submitted=date_submitted,
                    published=date_submitted,
                    status='published'
                )

                new_gpp.save()

                #
                # Installations
                #
                first = installation_types[install_type1]
                new_gpp.installations.add(first)
                if install_type2:
                    new_gpp.installations.add(installation_types[install_type2])
                if install_type3:
                    new_gpp.installations.add(installation_types[install_type3])


                #
                # Locations
                #
                # default to Unknown
                new_gpp.locations.add(location_options['Unknown'])

                #
                # Organizations
                #
                for idx in (1, 2, 3, 4):
                    org_id = row['Organization{}_ID'.format(idx)]
                    if org_id:
                        org = Organization.objects.get(account_num=org_id)
                        new_gpp.organizations.add(org)

                #
                # Topic
                #
                new_gpp.topics.add(energy_topic)


                # Tags
                tags_token = row['Tag(s)']
                tags = [tag.strip() for tag in tags_token.split(',')]
                for tag in tags:
                    new_gpp.keywords.add(tag)



                # Project Contact
                if row['ProjectContact-Name']:
                    Author.objects.create(
                        ct=new_gpp,
                        name=row['ProjectContact-Name'],
                        title=row['ProjectContact-Title'],
                        organization_id=int(row['ProjectContact-OrgID'])
                    )

                #
                # Uploads
                #
                if row['Upload 1']:
                    create_file_from_url(new_gpp, row['Upload 1'])
                if row['Upload 2']:
                    create_file_from_url(new_gpp, row['Upload 2'])

                #
                # URLs / Websites
                #
                for i in range(1, 6):
                    url = row['URL{}'.format(i)]
                    if url:
                        Website.objects.create(
                            url=url,
                            ct=new_gpp
                        )

                #
                # Submitter
                #
                submitter_email = row['Submitter email']
                try:
                    submitter_user = User.objects.get(email=submitter_email)
                except User.DoesNotExist:
                    submitter_user = user_monika

                new_gpp.submitted_by = submitter_user
                new_gpp.save()
