from hub.apps.content.models import CONTENT_TYPES
from iss.models import Organization
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = """
    Truncates the DB to 20 of each ContentType (for dev instances only!)

    This tool is useful for truncating a DB for use in a dev instance on a
    hobby dyno, which only allows small databases.

    Generally you would copy the production DB into the instance and then run
    this...

    heroku pg:copy aashe-hub-prod::HEROKU_POSTGRESQL_OLIVE_URL DATABASE_URL \
      --app your-dev-fork

    ***DO NOT RUN ON PRODUCTION***
    """

    def handle(self, *args, **options):

        confirm = raw_input(
            'This is a DESTRUCTIVE action. Are you sure? [y/N]: ')

        if confirm == 'y':
            print
            orgs = Organization.objects.all()
            orgs_to_delete = orgs[1000:]
            print "Deleting %d of %d organizations" % (orgs_to_delete.count(),
                                                       orgs.count())
            for org in orgs_to_delete:
                org.delete()
            for k, ctKlass in CONTENT_TYPES.items():
                to_delete = ctKlass.objects.all()[20:]
                print "Deleting %d of %d %s objects." % (
                    to_delete.count(), ctKlass.objects.count(), k)
                for obj in to_delete:
                    obj.delete()
            print
        else:
            print "Action Cancelled."
