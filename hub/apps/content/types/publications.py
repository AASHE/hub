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
        ('report', 'Report (Non-Student)'),
        ('thesis', 'Student Thesis/Dissertation'),
        ('other', 'Other Student Research Paper'),
    )

    cover_image = models.ImageField(blank=True, null=True, help_text=IMG_UPLOAD)

    release_date = models.DateField('Publication release date',
        blank=True, null=True, help_text='''Providing a release date is
        highly recommended.''')
    publisher = models.CharField('Publisher', max_length=200,
        blank=True, null=True, help_text='Enter the name of the publisher, if applicable.')
    periodical_name = models.CharField('Periodical/publication name',
        max_length=200, blank=True, null=True, help_text='''Enter the name of
        the periodical (e.g., journal, magazine, newspaper), if applicable. For
        book chapers, enter the title of the book.''')
    _type = models.CharField(max_length=40, choices=TYPE_CHOICES, null=True,
        verbose_name='Type of Material')

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'

    @classmethod
    def required_field_overrides(cls):
        return []

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
