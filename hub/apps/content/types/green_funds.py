from django.db import models

from hub.apps.metadata.models import SustainabilityTopic
from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex
from ..help import AFFIRMATION, FILE_UPLOAD


class GreenFund(ContentType):

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Green Fund'
        verbose_name_plural = 'Green Funds'

    @classmethod
    def exclude_form_fields(cls):
        return ['disciplines', 'submitted_by']

    @classmethod
    def label_overrides(cls):
        return {
            'date_created': 'Fund Creation Date',
        }

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'file': {'max': 3, 'min': 0},  # optional, up to 3
            'conditionally_required': {'website', 'file'}
        }

    @classmethod
    def initial_value_overrides(cls):
        return {
            'keywords': 'green funds'
        }

    @classmethod
    def preset_topics(cls):
        """
        Require "Energy" in topics
        """
        return [SustainabilityTopic.objects.get(name="Investment & Finance")]

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import GreenFundFilterSet
        return GreenFundFilterSet


class GreenFundIndex(BaseIndex):
    def get_model(self):
        return GreenFund
