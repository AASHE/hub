import requests
import tempfile
from django.core import files

from hub.apps.content.models import File


def create_file_from_url(parent, file_url):
    """
        Thanks:
        http://stackoverflow.com/questions/16174022/download-a-remote-image-and-save-it-to-a-django-model
    """
    
    # Steam the image from the url
    request = requests.get(file_url, stream=True)

    # Was the request OK?
    if request.status_code != requests.codes.ok:
        print "File Request Failed: %s" % file_url
        return
    print "requesting: %s" % file_url

    # Get the filename from the url, used for saving later
    file_name = file_url.split('/')[-1]
    if len(file_name) > 100:
        file_name = file_name[-100:-1]

    # Create a temporary file
    lf = tempfile.NamedTemporaryFile()

    # Read the streamed image in sections
    for block in request.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break

        # Write image block to temporary file
        lf.write(block)

    # Save the temporary file to the model#
    # This saves the model so be sure that is it valid
    file = File(ct=parent, label=file_name, affirmation=True)
    file.item.save(file_name, files.File(lf))
