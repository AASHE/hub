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
        ('presentation1', 'Presentation (1 speaker)'),
        ('presentation2plus', 'Presentation (2 or more speakers)'),
    )

    date = models.DateField('Presentation Date')
    conf_name = models.CharField('Conference Name', max_length=100,
        choices=CONF_NAME_CHOICES)
    presentation_type = models.CharField(max_length=100, blank=True, null=True,
        choices=PRESENTATION_CHOICES)
    document = models.FileField('Document Upload', help_text=FILE_UPLOAD,
        blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

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


class PresentationIndex(BaseIndex):
    def get_model(self):
        return Presentation
