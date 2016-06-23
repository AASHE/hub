from django.db import models

from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex
from ..help import AFFIRMATION


class CaseStudy(ContentType):
    background = models.TextField('Background',
        help_text='''Describe the circumstances that led to start-up of this
        project.''')
    goals = models.TextField('Project Goals',
        help_text='Describe the goals of this project.')
    implementation = models.TextField('Project Implementation',
        help_text='''Describe how the project was implemented, including who
        was involved.''')
    timeline = models.TextField('Project Timeline',
        help_text='''Describe how long this project took from start to finish
        and provide a list of key project milestones in chronological order.''')
    financing = models.TextField('Financing',
        help_text='''Describe the costs (both upfront and recurring) for each
        component of the project and explain how the project was financed.''')
    results = models.TextField('Project Results (or results to date)',
        help_text='''Describe the outcomes that resulted
        from the project implementation.''')
    lessons_learned = models.TextField('Lessons learned',
        help_text='''Describe what you learned though this project that would
        be helpful to others wishing to undertake a similar project.''')
    consider_for_award = models.BooleanField('Student Leadership Award',
        help_text='''Would you like this case study to be considered for an
        AASHE Student Leadership Award? The first author must be a student.''')

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Case Study'
        verbose_name_plural = 'Case Studies'

    @classmethod
    def label_overrides(cls):
        return {
            'description': 'Project Overview',
        }

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import CaseStudyBrowseFilterSet
        return CaseStudyBrowseFilterSet

    @classmethod
    def required_metadata(cls):
        return {
            'image': {'max': 5, 'min': 0},  # optional, up to 5
            'file': {'max': 3, 'min': 0},  # optional, up to 5
            'author': {'max': 5, 'min': 1},  # required, up to 5
            'website': {'max': 5, 'min': 0},  # optional, up to 5
        }

    @classmethod
    def required_field_overrides(cls):
        required_list = super(
            CaseStudy, cls).required_field_overrides()
        required_list.append('description')
        return required_list


class CaseStudyIndex(BaseIndex):
    def get_model(self):
        return CaseStudy
