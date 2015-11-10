from django.db import models
from model_utils import Choices

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from ..search import BaseIndex
from .strings import AFFIRMATION


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

    release_date = models.DateField(blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    periodical_name = models.CharField(max_length=200, blank=True, null=True)
    _type = models.CharField(max_length=40, choices=TYPE_CHOICES, blank=True, null=True,
        verbose_name='Type of Material')
    cover_image = models.ImageField(blank=True, null=True)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'


class PublicationIndex(BaseIndex):
    def get_model(self):
        return Publication
