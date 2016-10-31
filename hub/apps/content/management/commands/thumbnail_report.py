from hub.apps.content.models import Image

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Report how many images have been thumbnailed successfully"

    def handle(self, *args, **options):

        total_images = Image.objects.count()
        broken_small_thumbnail_count = 0
        broken_med_thumbnail_count = 0

        for i in Image.objects.all():
            if i.small_thumbnail == "/static/img/100x100_blank.png":
                broken_small_thumbnail_count += 1
            if i.med_thumbnail == "/static/img/300x300_blank.png":
                broken_med_thumbnail_count += 1

        print "Total images: %d" % total_images
        print "Broken small thumbs: %d" % broken_small_thumbnail_count
        print "Broken medium thumbs: %d" % broken_med_thumbnail_count
