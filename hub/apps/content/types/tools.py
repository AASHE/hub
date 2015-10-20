from django.db import models

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from .strings import AFFIRMATION


class Tool(ContentType):
    document = models.FileField(help_text="The following files formats are "
        "acceptable: PDF, Excel, Word, PPT...", blank=True, null=True)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'
