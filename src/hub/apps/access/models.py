from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class TemporaryUser(models.Model):
    """
    A user who is given temporary access as a "member"
    """
    email_address = models.EmailField()
    access_starts = models.DateField()
    access_ends = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email_address
