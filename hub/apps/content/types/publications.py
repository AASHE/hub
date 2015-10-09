from django.db import models
from model_utils import Choices

from ..models import ContentType
from ...metadata.models import InstitutionalOffice


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
    affirmation = models.BooleanField(default=False)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)

    @property
    def class_content_type(self):
        return self.CONTENT_TYPES.publication
