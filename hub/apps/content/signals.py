from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import (Author,
                     CONTENT_TYPES,
                     File,
                     Image)


@receiver(post_save, sender=Author, weak=False,
          dispatch_uid=('hub.apps.content.signals.author.post_save'
                        '.update_authors_search_data'))
@receiver(post_delete, sender=Author, weak=False,
          dispatch_uid=('hub.apps.content.signals.author.post_delete'
                        '.update_authors_search_data'))
def update_authors_search_data(sender, instance, **kwargs):
    """
    Update instance.ct.authors_search_data.
    """
    # Really only want to do this when instance.name changes, but maybe
    # that would require premature or impractical optimization -- namely
    # add a FieldTracker field for ContentType.name.  Or maybe that's a
    # good idea ... for later.
    content_type_model = CONTENT_TYPES[instance.ct.content_type]
    content_type = content_type_model.objects.get(
        pk=instance.ct.pk)
    content_type.authors_search_data = " ".join(
        [author.name for author in content_type.authors.all()
         if author.name]).strip()
    content_type.save()


@receiver(post_save, sender=File, weak=False,
          dispatch_uid='hub.apps.content.signals.file.post_save')
@receiver(post_delete, sender=File, weak=False,
          dispatch_uid='hub.apps.content.signals.file.post_delete')
def update_files_search_data(sender, instance, **kwargs):
    """
    Update instance.ct.files_search_data.
    """
    content_type_model = CONTENT_TYPES[instance.ct.content_type]
    content_type = content_type_model.objects.get(
        pk=instance.ct.pk)
    content_type.files_search_data = " ".join(
        [f.label for f in content_type.files.all()
         if f.label]).strip()
    content_type.save()


@receiver(post_save, sender=Image, weak=False,
          dispatch_uid='hub.apps.content.signals.image.post_save')
@receiver(post_delete, sender=Image, weak=False,
          dispatch_uid='hub.apps.content.signals.image.post_delete')
def update_images_search_data(sender, instance, **kwargs):
    """
    Update instance.ct.images_search_data.
    """
    content_type_model = CONTENT_TYPES[instance.ct.content_type]
    content_type = content_type_model.objects.get(
        pk=instance.ct.pk)
    content_type.images_search_data = " ".join(
        [image.caption for image in content_type.images.all()
         if image.caption]).strip()
    content_type.images_search_data += " " + " ".join(
        [image.credit for image in content_type.images.all()
         if image.credit]).strip()
    content_type.save()
