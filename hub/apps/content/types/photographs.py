from django.db import models

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from .strings import AFFIRMATION

class Photograph(ContentType):
    credit = models.CharField(max_length=500, blank=True, null=True)
    photo = models.ImageField(help_text="The following files formats are "
        "acceptable: JPEG, PNG, TIFF...", blank=True, null=True)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    @property
    def class_content_type(self):
        return self.CONTENT_TYPES.photograph
