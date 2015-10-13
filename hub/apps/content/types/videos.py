from django.db import models

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from .strings import AFFIRMATION


class Video(ContentType):
    link = models.URLField('Video Link', blank=True, null=True)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    @property
    def class_content_type(self):
        return self.CONTENT_TYPES.video
