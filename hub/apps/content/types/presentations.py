from django.db import models
from model_utils import Choices

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from ..search import BaseIndex
from ..help import AFFIRMATION


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
    document = models.FileField(help_text="The following files formats are "
        "acceptable: PDF, Excel, Word, PPT, JPEG, PNG...", blank=True, null=True)
    abstract = models.TextField(blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Conference Presentation'
        verbose_name_plural = 'Conference Presentations'

    @property
    def title_label(self):
        return 'Presentation Title'


class PresentationIndex(BaseIndex):
    def get_model(self):
        return Presentation
