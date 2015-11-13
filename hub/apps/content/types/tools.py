from django.db import models

from ..models import ContentType
from ..search import BaseIndex
from ..help import AFFIRMATION, FILE_UPLOAD


class Tool(ContentType):
    website = models.URLField('Website', blank=True, null=True)
    document = models.FileField('Document Upload',
        blank=True, null=True, help_text=FILE_UPLOAD + ''' Provide either a
        website or a publication document.''')
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'


class ToolIndex(BaseIndex):
    def get_model(self):
        return Tool
