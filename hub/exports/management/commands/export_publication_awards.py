from django.core.management.base import BaseCommand

from hub.apps.content.types.publications import Publication

import datetime


class Command(BaseCommand):
    help = 'Export for awards'

    def handle(self, *args, **options):

        START_DATE = datetime.date(year=2017, month=5, day=21)
        END_DATE = datetime.date(year=2018, month=5, day=19)

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
            "Sustainability Topic #1",
            "Sustainability Topic #2",
            "Sustainability Topic #3"
        ]

        print '\t'.join(pub_columns)

        pub_qs = Publication.objects.filter(
            date_created__gte=START_DATE,
            date_created__lte=END_DATE,
            status=Publication.STATUS_CHOICES.published,
            material_type__name__in=['Journal Article',
                                     'Graduate Student Research',
                                     'Undergraduate Student Research'])

        for p in pub_qs.order_by('material_type__name'):
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
            row.append(p.material_type.name)
            row.append(p.date_created)
            for i in range(3):
                try:
                    row.append(p.topics.all()[i])
                except IndexError:
                    row.append('')

            print '\t'.join([unicode(x) if x else '' for x in row])
