from hub.apps.content.models import Image
from hub.apps.content.tasks import thumbnail_image

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = """Create thumbnails for all
    """

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--recreate',
            action='store_true',
            dest='recreate',
            default=False,
            help='Force recreation of all thumbnails',
        )

    def handle(self, *args, **options):

        recreate = options['recreate']
        print "\n-------------------------"
        if recreate:
            print "Recreating thumbnails for %d Images" % Image.objects.count()
        else:
            print "Generating thumbnails for %d Images" % Image.objects.count()
        print "-------------------------\n"

        for i in Image.objects.all():
            if options['verbosity'] > 1:
                print "\nContent Type: %s\n" % i.ct.get_absolute_url()
            thumbnail_image.delay(
                i.pk,
                recreate=recreate,
                verbose=options['verbosity'] > 1)
