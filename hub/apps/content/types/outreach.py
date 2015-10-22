from django.db import models

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from .strings import AFFIRMATION


class OutreachMaterial(ContentType):
    document = models.FileField(help_text="The following files formats are "
        "acceptable: PDF, Excel, Word, PPT, JPEG, PNG...", blank=True, null=True)
    design_credit = models.CharField(max_length=500, blank=True, null=True)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Outreach Material'
        verbose_name_plural = 'Outreach Materials'
