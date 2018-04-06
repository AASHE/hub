import os.path
import csv
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from hub.apps.content.models import Website
from hub.apps.metadata.models import Organization, SustainabilityTopic, AcademicDiscipline, ProgramType
from hub.apps.content.types.academic import AcademicProgram


User = get_user_model()


class Command(BaseCommand):
    help = 'One time upload of academic programs'

    def handle(self, *args, **options):

        submitter_jade = User.objects.get(email='jade@aashe.org')
        date_submitted = datetime.date()

        with open("{}/{}".format(os.path.dirname(__file__), 'academic_programs_not_in_hub.csv'), 'rb') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:

                # may run into a date issue
                create_date = row['Year Founded (200x)'].date

                new_acad_prog = AcademicProgram(
                    title=row['Program Name'],
                    description=row['Description'],
                    outcomes=row['Learning Outcomes'],
                    completion=row['Expected completion time'],
                    num_students=row['Approx # students completing program annually'],
                    distance=row['Distance Ed.'],
                    commitment=row['Commitment'],
                    date_created=create_date,
                    date_submitted=date_submitted,
                    published=date_submitted,
                    status='published'
                )

                new_acad_prog.save()

                #
                # Organizations
                #
                for idx in (1, 2):
                    org_id = row['Organization{} ID'.format(idx)]
                    if org_id:
                        org = Organization.objects.get(account_num=org_id)
                        new_acad_prog.organizations.add(org)

                #
                # SustainabilityTopic
                #
                for idx in (1, 2):
                    tpic_name = row['Topic{}'.format(idx)]
                    if tpic_name:
                        tpic = SustainabilityTopic.objects.get(name=tpic_name)
                        new_acad_prog.topics.add(tpic)

                #
                # AcademicDiscipline
                #
                for idx in (1, 2, 3):
                    disc_name = row['Acad Discipline{}'.format(idx)]
                    if disc_name:
                        disc = AcademicDiscipline.objects.get(name=disc_name)
                        new_acad_prog.topics.add(disc)

                #
                # keywords
                #
                for idx in (1, 2, 3, 4):
                    tag_name = row['Tag{}'.format(idx)]
                    if tag_name:
                        new_acad_prog.keywords.add(tag_name)

                #
                # ProgramType
                #
                prog_name = row['Program Type']
                if prog_name:
                    prog = ProgramType.objects.get(name=prog_name)
                    new_acad_prog.program_type.add(prog)

                #
                # URLs / Websites
                #
                url = row['Link URL')]
                if url:
                    Website.objects.create(
                        url=url,
                        ct=new_acad_prog
                    )

                #
                # Submitter
                #
                new_acad_prog.submitted_by = submitter_jade
                new_acad_prog.save()
