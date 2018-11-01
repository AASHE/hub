import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from hub.apps.content.models import Author
from hub.apps.content.types.presentations import Presentation
from hub.apps.metadata.models import Organization, SustainabilityTopic, ConferenceName, PresentationType, \
    AcademicDiscipline, InstitutionalOffice
from hub.imports.utils import create_file_from_url

User = get_user_model()


class Command(BaseCommand):
    help = "One-time import of Conference Presentation data for 2018"

    def handle(self, *args, **options):

        with open("{}/{}".format(os.path.dirname(__file__), 'AASHE_2018_Presentations.csv'), 'rb') as csvfile:
            reader = csv.DictReader(csvfile)

            submitter_monika = User.objects.get(
                email='monika.urbanski@aashe.org')

            for row in reader:

                title = row['Presentation Title']
                description = row['Description or Abstract']
                conference_name = ConferenceName.objects.get(
                    name=row['ConferenceName'])
                presentation_type = PresentationType.objects.get(
                    name=row['PresType'])

                month, day, year = row['PresentationDate'].split('/')
                presentation = Presentation.objects.create(
                    title=title,
                    description=description,
                    conf_name=conference_name,
                    presentation_type=presentation_type,
                    date_created='{}-{}-{}'.format(year, month, day),
                    published=timezone.now(),
                    status='published',
                    submitted_by=submitter_monika
                )

                #
                # Academic Disciplines
                #
                for idx in (1, 2):
                    disc = row['Academic_Discipline_{}'.format(idx)]
                    if disc:
                        academic_discipline = AcademicDiscipline.objects.get(
                            name=disc)
                        presentation.disciplines.add(academic_discipline)

                #
                # Institutional office
                #
                for idx in (1, 2):
                    office_dept = row['OfficeDepartment{}'.format(idx)]
                    if office_dept:
                        office_dept = InstitutionalOffice.objects.get(
                            name=office_dept)
                        presentation.institutions.add(office_dept)

                #
                # Organizations
                #
                for idx in (1, 2, 3, 4, 5, 6, 7):
                    org_id = row['Org_{}_id'.format(idx)]
                    if org_id:
                        try:
                            org = Organization.objects.get(
                                membersuite_id=org_id)
                            presentation.organizations.add(org)
                        except Organization.DoesNotExist:
                            print "Org {} not found for {}".format(
                                org_id, title)

                #
                # Topics
                #
                for idx in (1, 2, 3):
                    topic = row['Topic_{}'.format(idx)]
                    if topic:
                        topic = SustainabilityTopic.objects.get(name=topic)
                        presentation.topics.add(topic)

                #
                # Tags
                #
                tags_token = row['Tags']
                tags = [tag.strip() for tag in tags_token.split(',')]
                for tag in tags:
                    presentation.keywords.add(tag)

                #
                # Authors
                #
                for idx in (1, 2, 3, 4, 5, 6, 7, 8):
                    author_name = row['Author{}_Name'.format(idx)].strip()
                    if author_name:
                        author_title = row['PositionTitle_{}'.format(idx)]
                        org_id = row['Author{}_Org_ID'.format(idx)]
                        org = None
                        if org_id:
                            try:
                                org = Organization.objects.get(
                                    membersuite_id=org_id)
                            except Organization.DoesNotExist:
                                print "Org {} not found for Author {} for {}".format(
                                    row['Author{}_Org_ID'.format(idx)], author_name, title)
                        Author.objects.create(
                            ct=presentation,
                            name=author_name,
                            title=author_title,
                            organization=org
                        )

                #
                # Files
                #
                for idx in (1, 2, 3, 4):
                    file_url = row['File{}_URL'.format(idx)]
                    if file_url:
                        create_file_from_url(
                            parent=presentation,
                            file_url=file_url,
                            image=False
                        )
