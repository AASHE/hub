from django.db import models
from model_utils import Choices

from ..search import BaseIndex
from ..models import ContentType
from ..help import AFFIRMATION, FILE_UPLOAD


class OutreachMaterial(ContentType):
    TYPE_CHOICES = Choices(
        ('logo', 'Logo'),
        ('signs/poster', 'Signs/Poster'),
        ('sticker', 'Sticker'),
        ('flyer', 'Flyer/Brochure'),
        ('guide', 'Guide'),
        ('map', 'Map'),
        ('other', 'Other'),
    )

    _type = models.CharField(max_length=40, choices=TYPE_CHOICES, blank=True, null=True,
        verbose_name='Type of Material')
    design_credit = models.CharField('Design credit (name and/or organization)',
        max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'Outreach Material'
        verbose_name_plural = 'Outreach Materials'

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'file': {'max': 3, 'min': 0},  # optional, up to 3
            'image': {'max': 5, 'min': 0},  # optional, up to 5
            'conditionally_required': {'website', 'file', 'image'}
        }


class OutreachMaterialIndex(BaseIndex):
    def get_model(self):
        return OutreachMaterial
