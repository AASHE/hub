from django.db import models
from model_utils import Choices

from ..models import ContentType
from ..search import BaseIndex
from ..help import AFFIRMATION, FILE_UPLOAD, IMG_UPLOAD


class Publication(ContentType):
    TYPE_CHOICES = Choices(
        ('book', 'Book'),
        ('book chapter', 'Book Chapter'),
        ('journal article', 'Journal Article'),
        ('news', 'News or Magazine Article'),
        ('blog', 'Blog Article'),
        ('report', 'Published Report'),
        ('graduate', 'Graduate Student Research'),
        ('undergrad', 'Undergraduate Student Research'),
    )

    publisher = models.CharField('Publisher', max_length=200,
        blank=True, null=True, help_text='Enter the name of the publisher, if applicable.')
    periodical_name = models.CharField('Periodical/publication name',
        max_length=200, blank=True, null=True, help_text='''Enter the name of
        the periodical (e.g., journal, magazine, newspaper), if applicable. For
        book chapers, enter the title of the book.''')
    _type = models.CharField(max_length=40, choices=TYPE_CHOICES, null=True,
        verbose_name='Type of Material',
        help_text='''"Journal Article," "Graduate Student Research" and
        "Undergraduate Student Research" submissions will be automatically
        considered for a Campus Sustainability Research Award as part of
        AASHE's annual awards program.''')

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        
    @classmethod
    def label_overrides(cls):
        return {
            'date_created': 'Publication Release Date',
        }

    @classmethod
    def required_field_overrides(cls):
        return []

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import PublicationBrowseFilterSet
        return PublicationBrowseFilterSet

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'author': {'max': 6, 'min': 1},  # required, up to 6
            'file': {'max': 3, 'min': 0},  # optional, up to 3
            'image': {'max': 5, 'min': 0},  # optional, up to 5
            'conditionally_required': {'website', 'file'}
        }


class PublicationIndex(BaseIndex):
    def get_model(self):
        return Publication
