import os.path
import csv
import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from hub.apps.content.models import Website
from hub.apps.metadata.models import (
    Organization,
    SustainabilityTopic,
    AcademicDiscipline,
    ProgramType,
)
from hub.apps.content.types.academic import AcademicProgram


User = get_user_model()


class Command(BaseCommand):
    help = "One time upload of academic programs updated for 2020 on Dec 16, 2020 by RZ"

    def handle(self, *args, **options):

        # submitter_jade = User.objects.get(email="jasmine@aashe.org")
        submitter_jade = User.objects.get(email="monika.urbanski@aashe.org ")
        date_submitted = datetime.datetime.now(tz=timezone.utc)
        with open(
            "{}/{}".format(
                os.path.dirname(__file__), "AcademicPrograms-2020-UPLOADDATA.csv"
            ),
            "rb",
        ) as csvfile:
            reader = csv.DictReader(csvfile)

            count = 1
            for row in reader:

                new_acad_prog = AcademicProgram(
                    title=row["Program Name"],
                    description=row["Description or Abstract"],
                    date_submitted=date_submitted,
                    published=date_submitted,
                    status="published",
                    permission="open",
                )

                new_acad_prog.save()

                for idx in (1, 2, 3):
                    tag = row["Tag{}".format(idx)]
                    if tag:
                        new_acad_prog.keywords.add(tag.strip())

                out = row["Learning Outcomes"]
                if out:
                    new_acad_prog.outcomes = out

                prog_name = row["Program Type"]
                if prog_name:
                    try:
                        prog = ProgramType.objects.get(name=prog_name.strip())
                        new_acad_prog.program_type = prog
                    except:
                        msg = "{}>>>>>new programtype:{}".format(new_acad_prog, prog)
                        self.stdout.write(self.style.ERROR(msg))

                comp = row["Expected Completion Time"]
                if comp:
                    new_acad_prog.completion = comp

                org_id = row["Organization1id".format(idx)]
                if org_id is not "":
                    org = Organization.objects.get(membersuite_id=org_id)
                    new_acad_prog.organizations.add(org)

                for idx in (1, 2):
                    topic_name = row["Sustainability Topic{}".format(idx)]
                    if topic_name:
                        try:
                            topic = SustainabilityTopic.objects.get(
                                name=topic_name.strip()
                            )
                            new_acad_prog.topics.add(topic)
                        except:
                            msg = "{}>>>>>new topic:{}".format(new_acad_prog, topic)
                            self.stdout.write(self.style.ERROR(msg))

                for idx in (1, 2, 3):
                    disc_name = row["Academic Discipline{}".format(idx)]
                    if disc_name:
                        disc = AcademicDiscipline.objects.get(name=disc_name)
                        new_acad_prog.disciplines.add(disc)

                website_label = row["Website1label"]
                website_url = row["Website1URL"]
                try:
                    Website.objects.create(
                        url=website_url, label=website_label, ct=new_acad_prog
                    )
                except:
                    msg = "{}>>>>>bad wesite:{}".format(new_acad_prog, website_label)
                    self.stdout.write(self.style.ERROR(msg))

                new_acad_prog.submitted_by = submitter_jade
                new_acad_prog.save()

                self.stdout.write(self.style.SUCCESS(count))
                count += 1

        return
