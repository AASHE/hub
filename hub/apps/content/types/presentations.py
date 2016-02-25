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

    date = models.DateField('Presentation Date', help_text='''If you don't know
    the exact day, choose the first day of the month. Use January 1 if you only
    know the year. You can use the calendar widget or type in a date in
    YYYY-MM-DD format.''')
    conf_name = models.CharField('Conference Name', max_length=100,
        choices=CONF_NAME_CHOICES, help_text='''If your conference is not
        listed, please select "other" and recommend a change by emailing
        resources@aashe.org''')
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
