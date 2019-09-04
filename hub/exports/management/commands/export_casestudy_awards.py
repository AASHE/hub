# Tip:
# PYTHONIOENCODING=UTF-8 ./manage.py export_casestudy_awards > casestudy_awards.tsv

from django.core.management.base import BaseCommand

from hub.apps.content.types.casestudies import CaseStudy

import datetime


class Command(BaseCommand):
    help = 'Export for awards'

    def handle(self, *args, **options):

        # By date created: June 20, 2015 - June 11, 2016
        START_DATE = datetime.date(year=2018, month=5, day=20)
        END_DATE = datetime.date(year=2019, month=5, day=22)

        pub_columns = [
            "Submission Title",
            "Submission URL",
            "Institutions",
            # "Submitter Name",
            "Submitter Email",
            "First Author Name",
            "First Author Title",
            "First Author Email",
            "First Author Organization",
            "First Author Org Is Member?",
            "First Author Org FTE",
            "First Author Org Type",
            "Student Leadership Award",
            "Date Submitted",
            "Sustainability Topic #1",
            "Sustainability Topic #2",
            "Sustainability Topic #3"
        ]

        print '\t'.join(pub_columns)

        casestudies = CaseStudy.objects.filter(
            date_submitted__gte=START_DATE,
            date_submitted__lte=END_DATE,
            status=CaseStudy.STATUS_CHOICES.published)

        for casestudy in casestudies.order_by('date_submitted'):
            row = []
            row.append(casestudy.title)
            row.append("https://hub.aashe.org%s" % casestudy.get_absolute_url())  # noqa
            row.append(", ".join([unicode(o) for o in casestudy.organizations.all()]))  # noqa
            row.append(casestudy.submitted_by.email)
            try:
                author = casestudy.authors.all()[0]
                row.append(author.name)
                row.append(author.title)
                row.append(author.email)
                if author.organization:
                    row.append(author.organization)
                    row.append(author.organization.is_member)
                    row.append(author.organization.enrollment_fte)
                    row.append(author.organization.org_type)
                else:
                    row.append('')
                    row.append('')
                    row.append('')
                    row.append('')
            except:
                row.append('')
                row.append('')
                row.append('')
            row.append(casestudy.consider_for_award)
            row.append(casestudy.date_submitted)
            for i in range(3):
                try:
                    row.append(casestudy.topics.all()[i])
                except IndexError:
                    row.append('')

            print '\t'.join([unicode(x) if x else '' for x in row])
