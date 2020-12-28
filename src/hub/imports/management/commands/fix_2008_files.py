from hub.apps.content.types.presentations import Presentation

from django.core.management.base import BaseCommand, CommandError
from django.core import files

import re
import requests
import tempfile


class Command(BaseCommand):
    help = 'Fix 2008 conference presentation imports'

    def handle(self, *args, **options):
        print "fixing files!"

        url_pattern = r'dl.php\?f=(\d+) Download.*'
        filename_pattern = r'.*filename=\"(.+)\"'
        url_prefix = "http://www2.aashe.org/conf2008/uploads/dl.php?f=%s"

        for p in Presentation.objects.filter(date__year=2008):
            for f in p.files.all():
                print f.label
                m = re.match(url_pattern, f.label)
                if m:
                    print 'Match found: ', m.group(1)
                    print p.get_absolute_url()
                    url = url_prefix % m.group(1)
                    request = requests.get(url, stream=True)
                    match = re.match(
                        filename_pattern,
                        request.headers['Content-disposition'])
                    file_name = match.group(1)
                    print "File Name: %s" % file_name
                    lf = tempfile.NamedTemporaryFile()
                    # Read the streamed image in sections
                    for block in request.iter_content(1024 * 8):
                        if not block:
                            break
                        lf.write(block)
                    f.label = file_name
                    f.item.save(file_name, files.File(lf))
                    f.save()
                else:
                    print 'No match'
