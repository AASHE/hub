from django.db import models


class TemporaryUser(models.Model):
    """
    A user who is given temporary access as a "member"
    """
    email_address = models.EmailField()
    access_starts = models.DateField()
    access_ends = models.DateField()
    notes = models.TextField(blank=True, null=True)
