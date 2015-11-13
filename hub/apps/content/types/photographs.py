from django.db import models

from ...metadata.models import InstitutionalOffice
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
    institutions = models.ManyToManyField(InstitutionalOffice, blank=True,
        verbose_name='Institution Office (if relevant)',
        help_text='''Only include if an office or division on campus is/was
        directly involved in the case study. Select up to three.''')

    class Meta:
        verbose_name = 'Photograph'
        verbose_name_plural = 'Photographs'


class PhotographIndex(BaseIndex):
    def get_model(self):
        return Photograph
