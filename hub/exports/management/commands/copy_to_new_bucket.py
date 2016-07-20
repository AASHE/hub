from django.core.management.base import BaseCommand, CommandError
from hub.apps.content.models import File, Image

import boto
from urlparse import urlparse


class Command(BaseCommand):
    help = 'Move all uploaded files to new bucket'

    def handle(self, *args, **options):

        conn = boto.connect_s3()
        src = conn.get_bucket('aashe-hub-dev')
        dst = conn.get_bucket('aashe-hub-production')

        for f in File.objects.filter(item__isnull=False):
            key = urlparse(f.item).path[1:]
            print "copying: %s" % key
            dst.copy_key(key, src.name, key)

        for i in Image.objects.filter(image__isnull=False):
            key = urlparse(i.image).path[1:]
            print "copying: %s" % key
            dst.copy_key(key, src.name, key)
