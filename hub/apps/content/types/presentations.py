from django.db import models
from model_utils import Choices

from ..models import ContentType
from ..search import BaseIndex
from ..help import AFFIRMATION, FILE_UPLOAD


class Presentation(ContentType):
    CONF_NAME_CHOICES = Choices(
        ('aashe', 'AASHE'),
        ('other', 'Other'),
    )
    PRESENTATION_CHOICES = Choices(
        ('poster', 'Poster'),
        ('presentation', 'Presentation'),
    )

    date = models.DateField('Presentation Date')
    conf_name = models.CharField('Conference Name', max_length=100,
        choices=CONF_NAME_CHOICES)
    presentation_type = models.CharField(max_length=100, blank=True, null=True,
        choices=PRESENTATION_CHOICES)

    class Meta:
        verbose_name = 'Conference Presentation'
        verbose_name_plural = 'Conference Presentations'

    @classmethod
    def label_overrides(cls):
        return {
            'title': 'Presentation Title',
            'description': 'Description or Abstract',
            'author': 'Presenter',
            'authors': 'Presenters',
        }

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'author': {'max': 6, 'min': 1},  # required, up to 6
            'file': {'max': 3, 'min': 1},  # required, up to 3
            'image': {'max': 5, 'min': 0},  # optional, up to 5
        }


class PresentationIndex(BaseIndex):
    def get_model(self):
        return Presentation
