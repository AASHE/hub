from django.db import models

from ..models import ContentType
from ..search import BaseIndex


class CenterAndInstitute(ContentType):
    num_paid = models.PositiveIntegerField('Number of paid staff employed at the center (FTE)',
        blank=True, null=True)
    founded = models.PositiveIntegerField('Year when center or institute was founded',
        blank=True, null=True, help_text='(e.g. 2009)')
    budget = models.PositiveIntegerField('Total operating budget for the center or institute (excluding salaries)?',
        blank=True, null=True, help_text='in U.S. dollars')

    class Meta:
        verbose_name = 'Research Center & Institute'
        verbose_name_plural = 'Research Centers & Institutes'

    @classmethod
    def label_overrides(cls):
        return {
            'title': 'Center Name',
        }

    @classmethod
    def required_field_overrides(cls):
        required_list = super(
            CenterAndInstitute, cls).required_field_overrides()
        required_list.append('disciplines')
        return required_list

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 1},  # required, up to 5
        }


class CenterAndInstituteIndex(BaseIndex):
    def get_model(self):
        return CenterAndInstitute
