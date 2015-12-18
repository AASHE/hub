from django.db import models

from ..models import ContentType
from ..search import BaseIndex
from ..help import AFFIRMATION


class CaseStudy(ContentType):
    background = models.TextField('Background', blank=True, null=True,
        help_text='''Describe the circumstances that led to the initiation of
        this project.''')
    goals = models.TextField('Project Goals', blank=True, null=True,
        help_text='Describe the goals of this project.')
    implementation = models.TextField('Project Implementation', blank=True, null=True,
        help_text='Describe the project and how it was implemented.')
    timeline = models.TextField('Project Timeline', blank=True, null=True,
        help_text='''Describe how long this project took from start to finish
        and provide a list of key project milestones in chronological order.''')
    financing = models.TextField('Financing', blank=True, null=True,
        help_text='''Describe the costs (both upfront and reoccurring) for each
        component of the project and explain how the project was financed.''')
    results = models.TextField('Project Results (or results to date)',
        blank=True, null=True, help_text='''Describe the outcomes that resulted
        from the project implementation.''')
    lessons_learned = models.TextField('Lessons learned', blank=True, null=True,
        help_text='''Describe the lessons learned from this project. This
        section may also be used to offer advice to others who wish to
        undertake a similar project.''')
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Case Study'
        verbose_name_plural = 'Case Studies'

    @classmethod
    def label_overrides(cls):
        return {
            'background': 'Project Overview',
        }


class CaseStudyIndex(BaseIndex):
    def get_model(self):
        return CaseStudy
