import sys

from hub.apps.content.models import File
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from urlparse import urlparse
from itertools import product

import boto


class Command(BaseCommand):
    help = """Output list of files to update"""

    def handle(self, *args, **options):

        src_bucket = "aashe-hub-production"
        
        for i in File.objects.all():
            if "+" in i.item or " " in i.item:
                print "FOUND: %s (%d)" % (i.item, i.id)
                print "\t%s" % i.ct.get_absolute_url()

                key = urlparse(i.item).path
                key = key.replace("/%s/" % src_bucket, "/")
                if key[0] == '/':
                    key = key[1:]
        
                our_file = find_object(
                    src_bucket,
                    key,
                    "aashe-hub-production",
                )
                print "FOUND: %s (%d)" % (i.item, i.id)
                print "\t%s" % i.ct.get_absolute_url()
                print our_file
        sys.exit(0)


# referenced from: http://stackoverflow.com/questions/2481685/
def find_object(src_bucket_name,
                src_key_name,
                dst_bucket_name,
                metadata=None,
                preserve_acl=True):
    

    s3 = boto.connect_s3()
    bucket = s3.lookup(src_bucket_name)

    # Lookup the existing object in S3
    key = bucket.lookup(src_key_name)
    if not key:
        key = bucket.lookup(src_key_name.replace('+', ' '))
        if not key:
            print "Basic lookup failed. Trying all options."
            all_options = get_all_options(src_key_name, '+', ' ')
            for k in list(all_options):
                key = bucket.lookup(k)
                if key:
                    break
    
    if not key:
        print "#######################"
        print "key failed: %s" % src_key_name
        return

    return key

def get_all_options(word, from_char, to_char):
    options = [(c,) if c != from_char else (from_char, to_char) for c in word]
    return (''.join(o) for o in product(*options))
    
