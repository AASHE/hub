from django.db import models
from model_utils import Choices

from ..models import ContentType
from ...metadata.models import ProgramType


class AcademicProgram(ContentType):
    DISTANCE_CHOICES = Choices(
        ('local', 'Local Only'),
        ('distance', 'Distance Education'),
        ('both', 'Both'),
    )
    COMMITMENT_CHOICES = Choices(
        ('full', 'Full-Time'),
        ('part', 'Part-Time'),
        ('both', 'Both'),
    )

    program_type = models.ForeignKey(ProgramType, blank=True, null=True, verbose_name='Program Type')
    outcomes = models.TextField('Learning Outcomes', blank=True, null=True)
    founded = models.PositiveIntegerField(blank=True, null=True)
    completion = models.CharField('Expected completion time', max_length=20, blank=True, null=True)
    num_students = models.PositiveIntegerField('Approximate number of students completing program annually', blank=True, null=True)
    distance = models.CharField('Distance Education', max_length=20, choices=DISTANCE_CHOICES, blank=True, null=True)
    commitment = models.CharField('Commitment', max_length=20, choices=COMMITMENT_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'Academic Program'
        verbose_name_plural = 'Academic Programs'

    @property
    def title_label(self):
        return 'Program Name'

