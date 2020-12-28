# Tip:
# PYTHONIOENCODING=UTF-8 ./manage.py export_casestudy_awards > casestudy_awards.tsv
"""
    Last Update Ro May28 2020
"""
from django.core.management.base import BaseCommand
from hub.apps.content.types.casestudies import CaseStudy

import datetime
import os
import string


class Command(BaseCommand):
    def handle(self, *args, **options):

        EXPORT_SETUP = {
            "START_DATE": datetime.date(year=2020, month=2, day=27),
            "END_DATE": datetime.date(year=2020, month=5, day=28),
            "OUTPUT_FILENAME": "hub-export-casetudy",
        }

        summary_output_file = open(
            EXPORT_SETUP["OUTPUT_FILENAME"] + str(datetime.datetime.now()) + ".tsv",
            "w+",
        )

        help = "Export for awards"

        column_headers = unicode(
            u"\t".join(
                [
                    "Submission Title",
                    "Submission URL",
                    "Institutions",
                    "Submitter Name",
                    "Submitter Email",
                    "First Author Name",
                    "First Author Email",
                    "First Author Organization",
                    "First Author Org Is Member?",
                    "First Author Org FTE",
                    "First Author Org Type",
                    "Student Leadership Award",
                    "Date Submitted",
                ]
            )
            .encode("utf-8")
            .strip()
        )

        print >> summary_output_file, column_headers

        casestudies = CaseStudy.objects.filter(
            # date_created__gte=EXPORT_SETUP["START_DATE"],
            # date_created__lte=EXPORT_SETUP["END_DATE"],
            status=CaseStudy.STATUS_CHOICES.published,
        )

        for casestudy in casestudies.order_by("date_created"):
            row = []

            row.append(casestudy.title)
            row.append("https://hub.aashe.org%s" % casestudy.get_absolute_url())  # noqa
            row.append(
                ", ".join([unicode(o) for o in casestudy.organizations.all()])
            )  # noqa
            submitterName = " ".join(
                [casestudy.submitted_by.first_name, casestudy.submitted_by.last_name,]
            )
            row.append(submitterName)
            row.append(casestudy.submitted_by.email)
            try:
                author = casestudy.authors.all()[0]
                row.append(author.name)
                row.append(author.email)
                if author.organization:
                    row.append(author.organization)
                    row.append(author.organization.is_member)
                    row.append(author.organization.enrollment_fte)
                    row.append(author.organization.institution_type)
                else:
                    row.append("NONE")
                    row.append("NO")
                    row.append("NONE")
                    row.append("INSTITUTION TYPE")
            except:
                row.append("EXCEPTION")
                row.append("EXCEPTION")
                row.append("EXCEPTION")
            row.append(casestudy.consider_for_award)
            row.append(casestudy.date_created)
            print(casestudy.date_created)

            print >> summary_output_file, u"\t".join(
                [unicode(x) if x else "" for x in row]
            ).encode("utf-8").strip()

        summary_output_file.close()
