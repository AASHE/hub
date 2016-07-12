from django.db import models
from model_utils import Choices

from ...metadata.models import ProgramType, SustainabilityTopic
from ..models import ContentType, ContentTypeManager
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

    program_type = models.ForeignKey(
        ProgramType, null=True, verbose_name='Program Type')
    outcomes = models.TextField('Learning Outcomes', blank=True, null=True,
        help_text="Consider completing if different from description.")
    completion = models.CharField('Expected completion time', max_length=128,
        blank=True, null=True, help_text='(e.g., "2.5 years" or "12 months")')
    num_students = models.PositiveIntegerField(
        'Approximate number of students completing program annually',
        blank=True, null=True, help_text="""Enter student headcounts instead of
        FTE. We recommend referring to Integrated Postsecondary Education Data
        System (IPEDS) data and including an average over five years.""")
    distance = models.CharField('Distance Education', max_length=20,
        choices=DISTANCE_CHOICES, blank=True, null=True)
    commitment = models.CharField('Commitment', max_length=20,
        choices=COMMITMENT_CHOICES, blank=True, null=True)

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Academic Program'
        verbose_name_plural = 'Academic Programs'

    @classmethod
    def label_overrides(cls):
        return {
            'title': 'Program Name',
            'description': 'Description',
            'author': 'Presenter',
            'authors': 'Presenters',
            'date_created': 'Year Founded',
        }

    @classmethod
    def required_field_overrides(cls):
        required_list = super(AcademicProgram, cls).required_field_overrides()
        required_list.append('disciplines')
        return required_list

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import AcademicBrowseFilterSet
        return AcademicBrowseFilterSet

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 1},  # required, up to 5
        }

    @classmethod
    def preset_topics(cls):
        """
        Require "Curriculum" in topics
        """
        return [SustainabilityTopic.objects.get(name="Curriculum")]


class AcademicProgramIndex(BaseIndex):
    def get_model(self):
        return AcademicProgram
