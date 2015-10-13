from django.db import models

from ..models import ContentType
from ...metadata.models import InstitutionalOffice


class Photograph(ContentType):
    credit = models.CharField(max_length=500, blank=True, null=True)
    photo = models.ImageField(help_text="The following files formats are "
        "acceptable: JPEG, PNG, TIFF...")
    affirmation = models.BooleanField(default=False)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)

    @property
    def class_content_type(self):
        return self.CONTENT_TYPES.photograph
