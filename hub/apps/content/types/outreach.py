from django.db import models
from model_utils import Choices

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from .strings import AFFIRMATION


class OutreachMaterial(ContentType):

    document = models.FileField(help_text="The following files formats are "
        "acceptable: PDF, Excel, Word, PPT, JPEG, PNG...")
    design_credit = models.CharField(max_length=500, blank=True, null=True)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    @property
    def class_content_type(self):
        return self.CONTENT_TYPES.outreach
