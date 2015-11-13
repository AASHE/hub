from django.db import models

from ..models import ContentType
from ..search import BaseIndex


class Video(ContentType):
    link = models.URLField('Video Link')

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    @classmethod
    def label_overrides(cls):
        return {
            'title': 'Video Title',
        }

class VideoIndex(BaseIndex):
    def get_model(self):
        return Video
