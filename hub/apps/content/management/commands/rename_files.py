from hub.apps.content.models import File

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from urlparse import urlparse
from itertools import product

import boto


class Command(BaseCommand):
    help = """Rename any files that have either a + or a space in them"""

    def handle(self, *args, **options):

        src_bucket = settings.AWS_STORAGE_BUCKET_NAME
        found_count = 0
        fixed_count = 0
        for i in File.objects.all():
            if "+" in i.item or " " in i.item:
                print "FOUND: %s (%d)" % (i.item, i.id)
                print "\t%s" % i.ct.get_absolute_url()
                found_count += 1

                old_key = urlparse(i.item).path
                old_key = old_key.replace("/%s/" % src_bucket, "/")
                if old_key[0] == '/':
                    old_key = old_key[1:]
                new_key = old_key.replace("+", "-")
                new_key = new_key.replace(" ", "_")

                new_file = copy_object(
                    src_bucket,
                    old_key,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    new_key,
                )

                if new_file:
                    i.item = new_file.generate_url(
                        expires_in=0, query_auth=False)
                    i.save()
                    fixed_count += 1

        print "#######################"
        print "FOUND: %d" % found_count
        print "FIXED: %d" % fixed_count


# referenced from: http://stackoverflow.com/questions/2481685/
def copy_object(src_bucket_name,
                src_key_name,
                dst_bucket_name,
                dst_key_name,
                metadata=None,
                preserve_acl=True):
    """
    Copy an existing object to another location.

    src_bucket_name   Bucket containing the existing object.
    src_key_name      Name of the existing object.
    dst_bucket_name   Bucket to which the object is being copied.
    dst_key_name      The name of the new object.
    metadata          A dict containing new metadata that you want
                      to associate with this object.  If this is None
                      the metadata of the original object will be
                      copied to the new object.
    preserve_acl      If True, the ACL from the original object
                      will be copied to the new object.  If False
                      the new object will have the default ACL.
    """
    print "copying %s to %s " % (src_key_name, dst_key_name)

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

    # Copy the key back on to itself, with new metadata
    try:
        return key.copy(
            dst_bucket_name, dst_key_name,
            metadata=metadata, preserve_acl=preserve_acl)
    except:
        print "#######################"
        print "copy failed for key: %s" % src_key_name
        return

def get_all_options(word, from_char, to_char):
    options = [(c,) if c != from_char else (from_char, to_char) for c in word]
    return (''.join(o) for o in product(*options))
    
