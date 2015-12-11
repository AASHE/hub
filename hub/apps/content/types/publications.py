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

    website = models.URLField('Website', blank=True, null=True)
    cover_image = models.ImageField(blank=True, null=True, help_text=IMG_UPLOAD)
    document = models.FileField('Document Upload',
        blank=True, null=True, help_text=FILE_UPLOAD + ''' Provide either a
        website or a publication document.''')
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

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


class PublicationIndex(BaseIndex):
    def get_model(self):
        return Publication
