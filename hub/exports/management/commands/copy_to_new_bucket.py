from django.core.management.base import BaseCommand, CommandError
from hub.apps.content.models import File, Image

import boto
from fish import ProgressFish
from urlparse import urlparse


class Command(BaseCommand):
    help = 'Move all uploaded files to new bucket'

    def handle(self, *args, **options):

        conn = boto.connect_s3()
        src = conn.get_bucket('aashe-hub-dev')
        dst = conn.get_bucket('aashe-hub-production')

        print "Copying all Files..."

        file_qs = File.objects.filter(item__isnull=False)
        fish = ProgressFish(total=file_qs.count())
        count = 0
        for f in file_qs[:3]:
            count += 1
            fish.animate(amount=count)
            key = urlparse(f.item).path[1:]
            dst.copy_key(key, src.name, key)

        print "Copying all Images..."

        image_qs = Image.objects.filter(image__isnull=False)
        fish2 = ProgressFish(total=image_qs.count())
        count = 0
        for i in image_qs[:3]:
            count += 1
            fish.animate(amount=count)
            key = urlparse(i.image).path[1:]
            dst.copy_key(key, src.name, key)

        print
