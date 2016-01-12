from django.db import models

from ..models import ContentType
from ..search import BaseIndex


class Video(ContentType):

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    @classmethod
    def label_overrides(cls):
        return {
            'title': 'Video Title',
        }

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 1},  # optional, up to 5
            'author': {'max': 5, 'min': 0},  # optional, up to 5
        }


class VideoIndex(BaseIndex):
    def get_model(self):
        return Video
