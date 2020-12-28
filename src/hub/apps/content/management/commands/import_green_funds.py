import os.path
import sys
import csv
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from hub.apps.content.types.green_funds import GreenFund
from hub.apps.content.models import Website
from hub.apps.metadata.models import (Organization, SustainabilityTopic,
                                      InstitutionalOffice, FundingSource)
from hub.imports.utils import create_file_from_url


User = get_user_model()


class Command(BaseCommand):
    help = "One-time import of Green Funds; Use the import_content settings"

    def handle(self, *args, **options):

        with open("{}/{}".format(os.path.dirname(__file__), 'Campus_Green_Funds_Master.csv'), 'rb') as csvfile:
            reader = csv.DictReader(csvfile)

            submitter_monika = User.objects.get(
                email='monika.urbanski@aashe.org')

            for row in reader:

                title = row['Title']
                description = row['Description']
                revolving = row['Revolving']

                month, day, year = row['FundCreatedDate'].split('/')
                greenfund = GreenFund.objects.create(
                    title=title,
                    description=description,
                    date_created='{}-{}-{}'.format(year, month, day),
                    published=timezone.now(),
                    status='published',
                    submitted_by=submitter_monika,
                    revolving_fund=revolving
                )

                #
                # Organizations
                #
                org_id = row['AmsOrgID']
                if org_id:
                    try:
                        org = Organization.objects.get(
                            membersuite_id=org_id)
                        greenfund.organizations.add(org)
                    except Organization.DoesNotExist:
                        print "Org {} not found for {}".format(
                            org_id, title)

                #
                # Sustainability Topics
                #
                topics_token = row['SustainabilityTopic(s)']
                topics = [topic.strip() for topic in topics_token.split(',')]
                for topic in topics:
                    t = SustainabilityTopic.objects.get(name=topic)
                    greenfund.topics.add(t)

                #
                # Tags
                #
                tags_token = row['Tag(s)']
                tags = [tag.strip() for tag in tags_token.split(',')]
                for tag in tags:
                    greenfund.keywords.add(tag)

                #
                # Funding Sources
                #

                funding_token = row['FundingSource(s)']
                sources = [source.strip()
                           for source in funding_token.split(',')]
                for source in sources:
                    s = FundingSource.objects.get(name=source)
                    greenfund.funding_sources.add(s)

                #
                # Student Fee
                # Get rid of the dollar sign, and cast to int
                if row['Fee']:
                    fee = row['Fee']
                    greenfund.student_fee = int(fee[1:])

                #
                # Budget
                # get rid of leading dollar sign, all commas and cast to int
                if row['Budget']:
                    budget = row['Budget']
                    new_budget = budget[1:].replace(',', '')
                    greenfund.annual_budget = int(new_budget)

                #
                # Files
                #
                if row['File_1_URL']:
                    create_file_from_url(
                        greenfund, row['File_1_URL'], label=row['File_1_Label'])
                if row['File_2_URL']:
                    create_file_from_url(
                        greenfund, row['File_2_URL'], label=row['File_2_Label'])

                #
                # URLs / Websites
                #
                if row['Website_1_URL']:
                    Website.objects.create(
                        url=row['Website_1_URL'],
                        ct=greenfund,
                        label=row['Website_1_Label']
                    )
                if row['Website_2_URL']:
                    Website.objects.create(
                        url=row['Website_2_URL'],
                        ct=greenfund,
                        label=row['Website_2_Label']
                    )

                greenfund.save()

                self.stdout.write(self.style.SUCCESS('Ok'))
            sys.exit(1)
