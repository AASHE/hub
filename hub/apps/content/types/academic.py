from django.db import models
from model_utils import Choices

from ...metadata.models import ProgramType
from ..models import ContentType
from ..search import BaseIndex


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

    program_type = models.ForeignKey(ProgramType, blank=True, null=True,
        verbose_name='Program Type')
    outcomes = models.TextField('Learning Outcomes', blank=True, null=True,
        help_text="Consider completing if different from description.")
    founded = models.PositiveIntegerField("Year Founded", blank=True, null=True,
        help_text="(e.g. 2009)")
    completion = models.CharField('Expected completion time', max_length=20,
        blank=True, null=True, help_text="(e.g. 2 years and 6 months)")
    num_students = models.PositiveIntegerField(
        'Approximate number of students completing program annually',
        blank=True, null=True, help_text="""We recommend referring to IPEDS data
        and including an average over five years.""")
    distance = models.CharField('Distance Education', max_length=20,
        choices=DISTANCE_CHOICES, blank=True, null=True)
    commitment = models.CharField('Commitment', max_length=20,
        choices=COMMITMENT_CHOICES, blank=True, null=True)

    class Meta:
        verbose_name = 'Academic Program'
        verbose_name_plural = 'Academic Programs'

    @classmethod
    def label_overrides(cls):
        return {
            'title': 'Program Name',
            'description': 'Description or Abstract',
            'author': 'Presenter',
            'author_plural': 'Presenters',
        }

    @classmethod
    def required_field_overrides(cls):
        return ['disciplines']

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import AcademicBrowseFilterSet
        return AcademicBrowseFilterSet


class AcademicProgramIndex(BaseIndex):
    def get_model(self):
        return AcademicProgram
