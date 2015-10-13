from django.db import models
from model_utils import Choices

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from .strings import AFFIRMATION


class Presentation(ContentType):
    CONF_NAME_CHOICES = Choices(
        ('aashe', 'AASHE'),
        ('other', 'Other'),
    )
    PRESENTATION_CHOICES = Choices(
        ('poster', 'Poster'),
        ('presentation1', 'Presentation (1 speaker)'),
        ('presentation2plus', 'Presentation (2 or more speaker)'),
    )

    date = models.DateField(blank=True, null=True)
    conf_name = models.CharField(max_length=100, blank=True, null=True,
        choices=CONF_NAME_CHOICES)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    presentation_type = models.CharField(max_length=100, blank=True, null=True,
        choices=PRESENTATION_CHOICES)
    abstract = models.TextField(blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    @property
    def title_label(self):
        return 'Presentation Title'

    @property
    def class_content_type(self):
        return self.CONTENT_TYPES.publication
