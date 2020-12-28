from django.db import models

from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex


class Video(ContentType):

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Video / Webinar'
        verbose_name_plural = 'Videos & Webinars'

    @classmethod
    def label_overrides(cls):
        return {
            'title': 'Video Title',
        }

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import VideoBrowseFilterSet
        return VideoBrowseFilterSet

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 1},  # optional, up to 5
            'author': {'max': 5, 'min': 0},  # optional, up to 5
            'file': {'max': 5, 'min': 0},  # optional, up to 5
        }


class VideoIndex(BaseIndex):
    def get_model(self):
        return Video
