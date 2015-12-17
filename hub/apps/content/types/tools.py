from django.db import models

from ..models import ContentType
from ..search import BaseIndex
from ..help import AFFIRMATION, FILE_UPLOAD


class Tool(ContentType):

    class Meta:
        verbose_name = 'Tool'
        verbose_name_plural = 'Tools'

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'author': {'max': 5, 'min': 0},  # optional, up to 6
            'file': {'max': 3, 'min': 0},  # optional, up to 3
            'conditionally_required': {'website', 'file'}
        }


class ToolIndex(BaseIndex):
    def get_model(self):
        return Tool
