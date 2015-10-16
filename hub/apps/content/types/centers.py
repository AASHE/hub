from django.db import models

from ...metadata.models import InstitutionalOffice
from ..models import ContentType


class CenterAndInstitute(ContentType):
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    num_paid = models.PositiveIntegerField('Number of Paid Staff', blank=True, null=True)
    founded = models.PositiveIntegerField('Year Founded', blank=True, null=True)
    budget = models.PositiveIntegerField('Total Budget', blank=True, null=True)

    @property
    def title_label(self):
        return 'Center Name'

    @property
    def class_content_type(self):
        return self.CONTENT_TYPES.center
