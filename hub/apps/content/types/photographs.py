from django.db import models

from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex
from ..help import AFFIRMATION, IMG_UPLOAD

class Photograph(ContentType):

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Photograph'
        verbose_name_plural = 'Photographs'

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import PhotographBrowseFilterSet
        return PhotographBrowseFilterSet

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'image': {'max': 5, 'min': 1},  # optional, up to 5
        }


class PhotographIndex(BaseIndex):
    def get_model(self):
        return Photograph
