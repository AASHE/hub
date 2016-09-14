from hub.apps.content.models import CONTENT_TYPES, Image, File, Website, Author
from hub.apps.metadata.models import (
    AcademicDiscipline, InstitutionalOffice, ProgramType, ConferenceName,
    PresentationType, CourseMaterialType, OutreachMaterialType,
    PublicationMaterialType, Organization)
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

            # start with Organization, as this will cascade heavily
            print "====================="
            print "Deleting Organizations"
            self.delete_objects_of_class(Organization, retain=100)
            print

            print "====================="
            print "Deleting Content Types"
            print
            for k, ctKlass in CONTENT_TYPES.items():
                self.delete_objects_of_class(ctKlass)
            print

            print "====================="
            print "Deleting Linked Objects and Metadata"
            class_list = [
                Image, File, Website, Author, AcademicDiscipline,
                InstitutionalOffice, ProgramType, ConferenceName,
                PresentationType, CourseMaterialType, OutreachMaterialType,
                PublicationMaterialType]
            for klass in class_list:
                self.delete_objects_of_class(klass)
        else:
            print "Action Cancelled."

    def delete_objects_of_class(self, klass, retain=20):
        to_delete = klass.objects.all()[retain:]
        print "Deleting %d of %d %s objects." % (
            to_delete.count(), klass.objects.count(), klass.__name__)
        for obj in to_delete:
            obj.delete()
