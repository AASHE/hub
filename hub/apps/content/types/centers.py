from django.db import models

from ...metadata.models import InstitutionalOffice
from ..models import ContentType
from ..search import BaseIndex


class CenterAndInstitute(ContentType):
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    num_paid = models.PositiveIntegerField('Number of Paid Staff', blank=True, null=True)
    founded = models.PositiveIntegerField('Year Founded', blank=True, null=True)
    budget = models.PositiveIntegerField('Total Budget', blank=True, null=True)

    class Meta:
        verbose_name = 'Research Center & Institute'
        verbose_name_plural = 'Research Centers & Institutes'

    @property
    def title_label(self):
        return 'Center Name'


class CenterAndInstituteIndex(BaseIndex):
    def get_model(self):
        return CenterAndInstitute
