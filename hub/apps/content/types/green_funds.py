from django.db import models

from hub.apps.metadata.models import SustainabilityTopic
from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex
from ..help import AFFIRMATION, FILE_UPLOAD


class GreenFund(ContentType):

    BOOL_CHOICES = (('Yes', 'Yes'), ('No', 'No'))

    objects = ContentTypeManager()

    funding_sources = models.ManyToManyField(
        'metadata.FundingSource',
        verbose_name='Primary Funding Source(s)',
        help_text="""Select up to three funding sources.""")

    # Changed to CharField from Bool as False became difficult to usefully apply in
    # browse filters
    revolving_fund = models.CharField(
        'Revolving Loan Fund',
        choices=BOOL_CHOICES,
        max_length=3,
        help_text="""Indicate "Yes" if this is a revolving loan fund (i.e.,
        the fund makes loans that are eventually repaid back into the fund).""")

    student_fee = models.IntegerField(null=True, blank=True)

    annual_budget = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Green Fund'
        verbose_name_plural = 'Green Funds'

    @classmethod
    def exclude_form_fields(cls):
        return ['disciplines', 'submitted_by']

    @classmethod
    def required_field_overrides(cls):
        required_list = super(
            GreenFund, cls).required_field_overrides()
        required_list.append('date_created')
        required_list.append('revolving_fund')
        return required_list

    @classmethod
    def label_overrides(cls):
        return {
            'date_created': 'Fund Creation Date',
            'student_fee': 'Typical Annual Fee per Student (US Dollars)',
            'annual_budget': 'Approximate Annual Budget (US Dollars)'
        }

    @classmethod
    def required_metadata(cls):
        return {
            'funding_sources': {'max': 3, 'min': 1},
            'website': {'max': 5, 'min': 0},  # optional, up to 5
            'file': {'max': 3, 'min': 0},  # optional, up to 3
            'conditionally_required': {'website', 'file'}
        }

    @classmethod
    def initial_value_overrides(cls):
        return {
            'keywords': 'green funds'
        }

    @classmethod
    def preset_topics(cls):
        """
        Require "Energy" in topics
        """
        return [SustainabilityTopic.objects.get(name="Investment & Finance")]

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import GreenFundFilterSet
        return GreenFundFilterSet


class GreenFundIndex(BaseIndex):
    def get_model(self):
        return GreenFund
