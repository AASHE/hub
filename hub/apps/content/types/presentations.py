from django.db import models
from model_utils import Choices

from ..models import ContentType, ContentTypeManager
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

    conf_name = models.CharField('Conference Name', max_length=100,
        choices=CONF_NAME_CHOICES, help_text='''If your conference is not
        listed, please select "other" and recommend a change by emailing
        resources@aashe.org''')
    presentation_type = models.CharField(max_length=100, blank=True, null=True,
        choices=PRESENTATION_CHOICES)

    objects = ContentTypeManager()

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
            'date_created': 'Presentation Date',
        }
        
    @classmethod
    def required_field_overrides(cls):
        required_list = super(
            Presentation, cls).required_field_overrides()
        required_list.append('date_created')
        return required_list

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import PresentationBrowseFilterSet
        return PresentationBrowseFilterSet

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
