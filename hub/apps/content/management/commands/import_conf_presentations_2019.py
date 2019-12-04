import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from hub.apps.content.models import Author
from hub.apps.content.types.presentations import Presentation
from hub.apps.metadata.models import Organization, SustainabilityTopic, ConferenceName, PresentationType, \
    AcademicDiscipline, InstitutionalOffice
from hub.imports.utils import create_file_from_path

User = get_user_model()


class Command(BaseCommand):
    help = "One-time import of Conference Presentation data for 2018"

    def handle(self, *args, **options):

        FILES_PATH = '/Users/tylor/src/aashe/files'

        with open("{}/{}".format(os.path.dirname(__file__), '2019_conf_pres.csv'), 'rb') as csvfile:
            reader = csv.DictReader(csvfile)

            submitter_monika = User.objects.get(email='monika.urbanski@aashe.org')
            conference_name = ConferenceName.objects.get(name='AASHE')

            for row in reader:

                title = row['Presentation_Title'].strip()
                description = row['Description'].strip()
                presentation_type = PresentationType.objects.get(
                    name=row['Presentation_Type'].strip())

                month, day, year = row['Presentation_Date'].split('/')
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
                disc = row['Academic_Discipline_1'].strip()
                if disc:
                    academic_discipline = AcademicDiscipline.objects.get(
                        name=disc)
                    presentation.disciplines.add(academic_discipline)
                    

                #
                # Institutional office
                #
                for idx in (1, 2):
                    office_dept = row['Office_Dept_{}'.format(idx)].strip()
                    if office_dept:
                        office_dept = InstitutionalOffice.objects.get(
                            name=office_dept)
                        presentation.institutions.add(office_dept)

                #
                # Organizations
                # Org_1_id
                for idx in (1, 2, 3, 4, 5, 6):
                    org_id = row['Org_{}_id'.format(idx)].strip()
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
                    topic = row['Topic_{}'.format(idx)].strip()
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
                        author_title = row['Position/Title _{}'.format(idx)]
                        org_id = row['Author_Org_{}_id'.format(idx)]
                        org = None
                        if org_id:
                            try:
                                org = Organization.objects.get(
                                    membersuite_id=org_id)
                            except Organization.DoesNotExist:
                                print "Org {} not found for Author {} for {}".format(org_id, author_name, title)
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
                    file_title = row['File{}_Title'.format(idx)].strip()
                    if file_title:
                        create_file_from_path(
                            parent=presentation,
                            files_dir=FILES_PATH,
                            path=file_title,
                            upload=False
                        )
                        
# 5192
