from django.db import models

from ..models import ContentType
from ..search import BaseIndex
from ..help import AFFIRMATION, IMG_UPLOAD

class Photograph(ContentType):
    image = models.ImageField(help_text=IMG_UPLOAD)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)
    credit = models.CharField('Photographer credit (name and/or organization',
        max_length=500, blank=True, null=True)
    caption = models.CharField('Caption description',
        max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'Photograph'
        verbose_name_plural = 'Photographs'

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'image': {'max': 5, 'min': 1},  # optional, up to 5
        }


class PhotographIndex(BaseIndex):
    def get_model(self):
        return Photograph
