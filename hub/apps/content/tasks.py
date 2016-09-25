from __future__ import absolute_import

from django.conf import settings
from celery import shared_task
from sorl.thumbnail import get_thumbnail

from .models import Image


@shared_task(name='content.thumbnail_image')
def thumbnail_image(image_id, recreate=False):
    """
        Takes an image object and populates the two thumbnail fields:

            small_thumbnail and med_thumbnail

        Note: passing the image id instead of the object itself because we're
        using json in the messages instead of pickle

        Note: this task has to happen in the view to avoid infinite recursion
        of the save method.

        @todo It should also happen in the admin, I guess???
    """
    image = Image.objects.get(pk=image_id)

    # Create the small thumbnail if it hasn't already been created
    default = Image._meta.get_field('small_thumbnail').get_default()
    if recreate or image.small_thumbnail == default:
        thmb = get_thumbnail(image.image, '100x100', crop='center', quality=99)
        image.small_thumbnail = "%s%s" % (settings.MEDIA_URL, thmb.name)

    # Create the medium thumbnail if it hasn't already been created
    default = Image._meta.get_field('med_thumbnail').get_default()
    if recreate or image.med_thumbnail == default:
        thmb = get_thumbnail(image.image, '300x300', crop='center', quality=99)
        image.med_thumbnail = "%s%s" % (settings.MEDIA_URL, thmb.name)

    image.save()
