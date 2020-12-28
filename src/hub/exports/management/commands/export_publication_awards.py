from django.core.management.base import BaseCommand
from hub.apps.content.types.publications import Publication
import datetime

"""
    Last Update Ro May28 2020
"""


class Command(BaseCommand):
    help = "Export for awards"

    def handle(self, *args, **options):

        EXPORT_SETUP = {
            "START_DATE": datetime.date(year=2015, month=3, day=7),
            "END_DATE": datetime.date(year=2020, month=5, day=18),
            "OUTPUT_FILENAME": "hub-export-publications",
        }

        summary_output_file = open(
            EXPORT_SETUP["OUTPUT_FILENAME"] + str(datetime.datetime.now()) + ".tsv",
            "w+",
        )

        column_headers = unicode(
            u"\t".join(
                [
                    "Category",
                    "Submission Title",
                    "Submission URL",
                    "Institutions",
                    "Submitter Email",
                    "First Author Name",
                    "First Author Email",
                    "First Author Organization",
                    "Type of Material",
                    "Date Created",
                    "Sustainability Topic #1",
                    "Sustainability Topic #2",
                    "Sustainability Topic #3",
                ]
            )
            .encode("utf-8")
            .strip()
        )

        print >> summary_output_file, column_headers

        pub_qs = Publication.objects.filter(
            # date_created__gte=START_DATE,
            # date_created__lte=END_DATE,
            status=Publication.STATUS_CHOICES.published,
            material_type__name__in=[
                "Journal Article",
                "Graduate Student Research",
                "Undergraduate Student Research",
            ],
        )

        for p in pub_qs.order_by("material_type__name"):
            row = []
            row.append(p.material_type)
            row.append(p.title)
            row.append("https://hub.aashe.org%s" % p.get_absolute_url())
            row.append(", ".join([unicode(o) for o in p.organizations.all()]))
            row.append(p.submitted_by.email)
            try:
                author = p.authors.all()[0]
                row.append(author.name)
                row.append(author.email)
                row.append(author.organization)
            except:
                row.append("NONE")
                row.append("NONE")
                row.append("NONE")
            row.append(p.material_type.name)
            row.append(p.date_created)
            for i in range(3):
                try:
                    row.append(p.topics.all()[i])
                except IndexError:
                    row.append("NO TOPIC")

            print >> summary_output_file, u"\t".join(
                [unicode(x) if x else "" for x in row]
            ).encode("utf-8").strip()

        summary_output_file.close()
