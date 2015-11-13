from django.db import models
from model_utils import Choices

from ...metadata.models import ProgramType, InstitutionalOffice
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
    institutions = models.ManyToManyField(InstitutionalOffice, blank=True,
        verbose_name='Institution Office (if relevant)',
        help_text='''Only include if an office or division on campus is directly
        tied to this academic program. Select up to three.''')

    class Meta:
        verbose_name = 'Academic Program'
        verbose_name_plural = 'Academic Programs'

    @property
    def title_label(self):
        return 'Program Name'

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import AcademicBrowseFilterSet
        return AcademicBrowseFilterSet


class AcademicProgramIndex(BaseIndex):
    def get_model(self):
        return AcademicProgram
