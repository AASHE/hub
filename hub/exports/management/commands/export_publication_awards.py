from django.core.management.base import BaseCommand, CommandError

from hub.apps.content.types.publications import Publication

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
            # "First Author Title",
            "First Author Email",
            "First Author Organization",
            "Type of Material",
            "Date Created",
        ]

        print '\t'.join(pub_columns)

        pub_qs = Publication.objects.filter(
            date_created__gte=START_DATE,
            date_created__lte=END_DATE,
            status=Publication.STATUS_CHOICES.published,
            _type__in=['journal article', 'graduate', 'undergrad'])

        for p in pub_qs.order_by('_type'):
            row = []
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
                row.append('')
                row.append('')
                row.append('')
            row.append(p._type)
            row.append(p.date_created)
            print '\t'.join([unicode(x) if x else '' for x in row])
        