from django.db import models

from ..models import ContentType
from ..search import BaseIndex


class Video(ContentType):
    link = models.URLField('Video Link', blank=True, null=True)

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'


class VideoIndex(BaseIndex):
    def get_model(self):
        return Video
