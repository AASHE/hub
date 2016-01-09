from django.db import models

from ..models import ContentType
from ..search import BaseIndex
from ..help import AFFIRMATION


class CaseStudy(ContentType):
    background = models.TextField('Background',
        help_text='''Describe the circumstances that led to the initiation of
        this project.''')
    goals = models.TextField('Project Goals',
        help_text='Describe the goals of this project.')
    implementation = models.TextField('Project Implementation',
        help_text='Describe the project and how it was implemented.')
    timeline = models.TextField('Project Timeline',
        help_text='''Describe how long this project took from start to finish
        and provide a list of key project milestones in chronological order.''')
    financing = models.TextField('Financing',
        help_text='''Describe the costs (both upfront and reoccurring) for each
        component of the project and explain how the project was financed.''')
    results = models.TextField('Project Results (or results to date)',
        blank=True, null=True, help_text='''Describe the outcomes that resulted
        from the project implementation.''')
    lessons_learned = models.TextField('Lessons learned',
        help_text='''Describe the lessons learned from this project. This
        section may also be used to offer advice to others who wish to
        undertake a similar project.''')

    class Meta:
        verbose_name = 'Case Study'
        verbose_name_plural = 'Case Studies'

    @classmethod
    def label_overrides(cls):
        return {
            'description': 'Project Overview',
        }

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
