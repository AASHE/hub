from django.db import models
from model_utils import Choices

from ...metadata.models import SustainabilityTopic, CourseMaterialType
from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex
from ..help import AFFIRMATION, FILE_UPLOAD


class Material(ContentType):
    LEVEL_CHOICES = Choices(
        ('introductory', 'Introductory'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    material_type = models.ForeignKey(
        CourseMaterialType, null=True, verbose_name='Type of Material',
        help_text='Select the best option.',)
    course_name = models.CharField(
        'Course Name', max_length=500, blank=True, null=True)
    course_level = models.CharField(
        'Course Level', max_length=50, blank=True, null=True,
        choices=LEVEL_CHOICES,
        help_text='''100-level courses (or equivalents) may be designated as
        introductory, 200- or 300-level as intermediate, and 400-level or
        graduate courses as advanced.''')

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Course Material'
        verbose_name_plural = 'Course Materials'

    @classmethod
    def required_field_overrides(cls):
        required_list = super(Material, cls).required_field_overrides()
        required_list.append('disciplines')
        return required_list

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import MaterialBrowseFilterSet
        return MaterialBrowseFilterSet

    @classmethod
    def required_metadata(cls):
        return {
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'author': {'max': 5, 'min': 0},  # optional, up to 5
            'file': {'max': 3, 'min': 0},  # optional, up to 3
            'conditionally_required': {'website', 'file'}
        }

    @classmethod
    def preset_topics(cls):
        """
        Require "Curriculum" in topics
        """
        return [SustainabilityTopic.objects.get(name="Curriculum")]


class MaterialIndex(BaseIndex):
    def get_model(self):
        return Material
