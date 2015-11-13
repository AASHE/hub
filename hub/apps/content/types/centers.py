from django.db import models

from ..models import ContentType
from ..search import BaseIndex


class CenterAndInstitute(ContentType):
    website = models.URLField('Website')
    num_paid = models.PositiveIntegerField('Number of paid staff employed at the center (FTE)',
        blank=True, null=True)
    founded = models.PositiveIntegerField('Year when center or institute was founded',
        blank=True, null=True, help_text='(e.g. 2009)')
    budget = models.PositiveIntegerField('Total operating budget for the center or institute (excluding salaries)?',
        blank=True, null=True, help_text='in U.S. dollars')

    class Meta:
        verbose_name = 'Research Center & Institute'
        verbose_name_plural = 'Research Centers & Institutes'

    @property
    def title_label(self):
        return 'Center Name'


class CenterAndInstituteIndex(BaseIndex):
    def get_model(self):
        return CenterAndInstitute
