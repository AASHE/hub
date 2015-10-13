from django.db import models

from ..models import ContentType
from ...metadata.models import ProgramType, InstitutionalOffice
from .strings import AFFIRMATION


class CaseStudy(ContentType):
    program_type = models.ForeignKey(ProgramType, blank=True, null=True, verbose_name='Program Type')
    overview = models.TextField('Project overview', blank=True, null=True)
    background = models.TextField('Background', blank=True, null=True)
    goals = models.TextField('Project Goals', blank=True, null=True)
    implementation = models.TextField('Project Implementation', blank=True, null=True)
    timeline = models.TextField('Project Timeline', blank=True, null=True)
    financing = models.TextField('Financing', blank=True, null=True)
    results = models.TextField('Project Results (or results to date)', blank=True, null=True)
    lessons_learned = models.TextField('Lessons learned', blank=True, null=True)
    institution = models.ForeignKey(InstitutionalOffice, blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    @property
    def class_content_type(self):
        return self.CONTENT_TYPES.casestudy