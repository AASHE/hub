import os.path
import csv
import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from hub.apps.content.models import Website
from hub.apps.metadata.models import Organization, SustainabilityTopic, AcademicDiscipline, ProgramType
from hub.apps.content.types.academic import AcademicProgram


User = get_user_model()


class Command(BaseCommand):
    help = 'One time upload of academic programs'

    def handle(self, *args, **options):

        submitter_jade = User.objects.get(email='jade@aashe.org')
        date_submitted = datetime.datetime.now(tz=timezone.utc)

        with open("{}/{}".format(os.path.dirname(__file__), 'academic_programs_not_in_hub.csv'), 'rb') as csvfile:
            reader = csv.DictReader(csvfile)

            count = 1
            for row in reader:

                new_acad_prog = AcademicProgram(
                    title=row['Program Name '],
                    description=row['Description'],
                    date_submitted=date_submitted,
                    published=date_submitted,
                    status='published'
                )

                new_acad_prog.save()


                # outcomes=row['Learning Outcomes'],
                #
                #
                out = row['Learning Outcomes']
                if out:
                    new_acad_prog.outcomes = out

                # commitment=row['Commitment'],
                #
                #
                com = row['Commitment']
                if com:
                    new_acad_prog.commitment = com

                # distance=row['Distance Ed.'],
                #
                #
                dis = row['Distance Ed.']
                if dis:
                    new_acad_prog.distance = dis

                # num_students=row['Approx # students completing program annually'],
                #
                #
                stud = row['Approx # students completing program annually']
                if stud is not '':
                    new_acad_prog.num_students = int(stud)

                # completion=row['Expected completion time'],
                #
                #
                comp = row['Expected completion time']
                if comp:
                    new_acad_prog.completion = comp

                #
                # date_created
                #
                d = row['Year Founded (200x)']
                if d:
                    create_date = datetime.date(int(d), 1, 1)
                    new_acad_prog.date_created = create_date

                #
                # Organizations
                #
                for idx in (1, 2):
                    org_id = row['Organization{} ID'.format(idx)]
                    if org_id is not '':
                        # if len(org_id) is 3:
                        #     new_org_id = '0' + org_id
                        #     org = Organization.objects.get(membersuite_id=new_org_id)
                        # else:
                        org = Organization.objects.get(membersuite_id=org_id)

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
                        new_acad_prog.disciplines.add(disc)

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
                    new_acad_prog.program_type = prog

                #
                # URLs / Websites
                #
                url = row['Link URL']
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

                self.stdout.write(self.style.SUCCESS(count))
                count += 1

        return
