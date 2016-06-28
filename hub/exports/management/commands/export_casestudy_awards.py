from django.core.management.base import BaseCommand, CommandError

from hub.apps.content.types.casestudies import CaseStudy

import datetime


class Command(BaseCommand):
    help = 'Export for awards'
    
    def handle(self, *args, **options):

        # By date created: June 20, 2015 - June 11, 2016
        START_DATE = datetime.date(year=2015, month=6, day=20)
        END_DATE = datetime.date(year=2016, month=6, day=11)

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
            "Student Leadership Award",
            "Date Created",
        ] 

        print '\t'.join(pub_columns)

        cs_qs = CaseStudy.objects.filter(
            # date_created__gte=START_DATE,
            date_created__lte=END_DATE,
            status=CaseStudy.STATUS_CHOICES.published)

        for cs in cs_qs.order_by('date_created'):
            row = []
            row.append(cs.title)
            row.append("https://hub.aashe.org%s" % cs.get_absolute_url())
            row.append(", ".join([unicode(o) for o in cs.organizations.all()]))
            row.append(cs.submitted_by.email)
            try:
                author = cs.authors.all()[0]
                row.append(author.name)
                row.append(author.title)
                row.append(author.email)
                if author.organization:
                    row.append(author.organization)
                    row.append(author.organization.is_member)
                    row.append(author.organization.enrollment_fte)
                else:
                    row.append('')
                    row.append('')
                    row.append('')
            except:
                row.append('')
                row.append('')
                row.append('')
            row.append(cs.consider_for_award)
            row.append(cs.date_created)
            
            print '\t'.join([unicode(x) if x else '' for x in row])
        