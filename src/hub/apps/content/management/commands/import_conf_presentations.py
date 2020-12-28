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
    help = "One-time import of Conference Presentation data; Use the import_content settings"

    def handle(self, *args, **options):

        FILES_PATH = '/Users/brian/virtualenvs/AASHE/src/hub/conf_presentations'
        with open("{}/{}".format(os.path.dirname(__file__), 'conference_presentations.csv'), 'rb') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:

                title = row['Presentation Title']
                description = row['Description or Abstract']
                conference_name = ConferenceName.objects.get(name=row['ConferenceName'])
                presentation_type = PresentationType.objects.get(name=row['PresType'])

                month, day, year = row['PresentationDate'].split('/')
                presentation = Presentation.objects.create(
                    title=title,
                    description=description,
                    conf_name=conference_name,
                    presentation_type=presentation_type,
                    date_created='{}-{}-{}'.format(year, month, day),
                    published=timezone.now(),
                    status='published'
                )

                #
                # Academic Disciplines
                #
                disc = row['AcademicDiscipline1']
                if disc:
                    academic_discipline = AcademicDiscipline.objects.get(name=disc)
                    presentation.disciplines.add(academic_discipline)

                #
                # Institution
                #
                office_dept1 = row['OfficeDepartment1']
                if office_dept1:
                    office_dept1 = InstitutionalOffice.objects.get(name=office_dept1)
                    presentation.institutions.add(office_dept1)

                #
                # Organizations
                #
                for idx in (1, 2, 3, 4, 5, 6, 7):
                    org_id = row['Organization{}_id'.format(idx)]
                    if org_id:
                        try:
                            org = Organization.objects.get(membersuite_id=org_id)
                            presentation.organizations.add(org)
                        except Organization.DoesNotExist:
                            print "Org {} not found for {}".format(org_id, title)


                #
                # Topics
                #
                for idx in (1, 2, 3):
                    topic = row['SustainabilityTopic{}'.format(idx)]
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
                        author_title = row['Author{}_Title'.format(idx)]
                        org_id = row['Author{}_OrgID'.format(idx)]
                        org = None
                        if org_id:
                            try:
                                org = Organization.objects.get(membersuite_id=org_id)
                            except Organization.DoesNotExist:
                                print "Org {} not found for Author {} for {}".format(row['Author{}_OrgID'.format(idx)], author_name, title)
                        Author.objects.create(
                            ct=presentation,
                            name=author_name,
                            title=author_title,
                            organization=org
                        )

                #
                # Files
                #
                for f in (1, 2, 3, 4):
                    file_name = 'File{}'.format(f)
                    if row[file_name]:
                        create_file_from_path(
                            presentation,
                            FILES_PATH,
                            row[file_name],
                            upload=False
                        )

