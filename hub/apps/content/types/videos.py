from django.db import models

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from ..search import BaseIndex
from ..help import AFFIRMATION


class Video(ContentType):
    link = models.URLField('Video Link', blank=True, null=True)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'


class VideoIndex(BaseIndex):
    def get_model(self):
        return Video
