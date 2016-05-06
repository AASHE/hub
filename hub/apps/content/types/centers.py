from django.db import models

from ...metadata.models import SustainabilityTopic
from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex


class CenterAndInstitute(ContentType):
    num_paid = models.PositiveIntegerField('Number of paid staff employed at the center (FTE)',
        blank=True, null=True)
    budget = models.PositiveIntegerField('Total operating budget for the center or institute (excluding salaries)?',
        blank=True, null=True, help_text='in U.S. dollars')

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Research Center & Institute'
        verbose_name_plural = 'Research Centers & Institutes'

    @classmethod
    def label_overrides(cls):
        return {
            'title': 'Center Name',
            'date_created': 'Date Founded',
        }

    @classmethod
    def required_field_overrides(cls):
        required_list = super(
            CenterAndInstitute, cls).required_field_overrides()
        required_list.append('disciplines')
        return required_list

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import CenterAndInstituteBrowseFilterSet
        return CenterAndInstituteBrowseFilterSet

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 1},  # required, up to 5
        }

    @classmethod
    def preset_topics(cls):
        """
        Require "Research" in topics
        """
        return [SustainabilityTopic.objects.get(name="Research")]


class CenterAndInstituteIndex(BaseIndex):
    def get_model(self):
        return CenterAndInstitute
