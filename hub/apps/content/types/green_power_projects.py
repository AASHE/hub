from django.db import models

from hub.apps.metadata.models import SustainabilityTopic
from hub.apps.submit.forms import SubmitResourceForm
from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex


class GreenPowerProject(ContentType):


    OWNERSHIP_TYPES = (
        ('unknown', 'Unknown'),
        ('institution-owned', 'Institution Owned'),
        ('third-party-lease', 'Third-party owned (lease)'),
        ('third-party-purchase', 'Third-party owned (power purchase agreement)'),
    )
    MONEY_SAVER_OPTIONS = (
        ('yes', 'Yes'),
        ('no', 'No'),
        ('unknown', 'Unknown')
    )
    PPA_CHOICES = (
        ('< 3', '<$0.03'),
        ('4 - 4.9', '$0.04-0.049'),
        ('5 - 5.9', '$0.05-0.059'),
        ('6 - 6.9', '$0.06-0.069'),
        ('7 - 7.9', '$0.07-0.079'),
        ('8 - 8.9', '$0.08-0.089'),
        ('9 - 9.9', '$0.09-0.099'),
        ('10 - 10.9', '$0.10-$0.109'),
        ('11 - 11.9', '$0.11-$0.119'),
        ('> 12', '>$12'),
    )

    PPA_ESCALATOR_CHOICES = (
        ('0 (i.e., no annual escalator)', '0 (i.e., no annual escalator)'),
        ('0.01% to 1%', '0.01% to 1%'),
        ('1% to 1.49%', '1% to 1.49%'),
        ('1.5% to 1.99%', '1.5% to 1.99%'),
        ('2% to 2.49%', '2% to 2.49%'),
        ('2.5% to 2.99%', '2.5% to 2.99%'),
        ('3% to 4%', '3% to 4%'),
        ('Greater than 4%', 'Greater than 4%')
    )

    project_size = models.CharField(max_length=50)
    annual_production = models.CharField(max_length=50, blank=True, null=True)
    installed_cost = models.CharField(max_length=50, blank=True, null=True)
    date_installed = models.DateField(blank=True, null=True)

    # Required, 3 max
    installations = models.ManyToManyField(
        'metadata.GreenPowerInstallation',
        verbose_name='Installation Type',
        help_text='Select up to three'
    )

    # Required, select 1
    ownership_type = models.CharField(max_length=200, choices=OWNERSHIP_TYPES)

    # Optional, 3 max
    finance_sources = models.ManyToManyField(
        'metadata.GreenPowerFinanceOption',
        verbose_name='Source(s) of Financing',
        help_text='Select up to 3',
        blank=True
    )
    # Required, 2 max
    locations = models.ManyToManyField(
        'metadata.GreenPowerLocation',
        verbose_name='Project Location',
        help_text='Select up to 2'
    )
    money_saver = models.CharField(max_length=100, choices=MONEY_SAVER_OPTIONS, blank=True, null=True)
    cost_savings_desc = models.TextField(blank=True, null=True)
    starting_ppa_price = models.CharField(blank=True, null=True, max_length=50, choices=PPA_CHOICES)
    ppa_escalator = models.CharField(blank=True, null=True, max_length=50, choices=PPA_ESCALATOR_CHOICES)
    ppa_escalator_desc = models.TextField(blank=True, null=True)
    ppa_duration = models.PositiveIntegerField(blank=True, null=True)

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Green Power Project'
        verbose_name_plural = 'Green Power Projects'

    @classmethod
    def exclude_form_fields(cls):
        """
        `topics` field is excluded because instances will belong to Energy topic
        """
        return ['disciplines']

    @classmethod
    def get_custom_filterset(cls):
        from ...browse.filterset import GreenPowerBrowseFilterSet
        return GreenPowerBrowseFilterSet

    @classmethod
    def label_overrides(cls):
        return {
            'description': 'Description / Project Overview',
            'project_size': 'Project size (kW)',
            'annual_production': 'Estimated Annual Production (kWh)',
            'installed_cost': 'Installed Cost (US Dollars)',
            'date_installed': 'Project installation date',
            'money_saver': 'Is the project expected to save money for the institution overall?',
            'cost_savings_desc': 'Description of cost savings and calculation methods',
            'starting_ppa_price': 'Starting PPA price, if applicable',
            'ppa_escalator': 'Annual PPA price escalator',
            'ppa_escalator_desc': 'PPA escalator description',
            'ppa_duration': 'Duration of PPA in years',
            'authors': 'Project Contacts'
        }

    @classmethod
    def preset_topics(cls):
        """
        Require "Energy" in topics
        """
        return [SustainabilityTopic.objects.get(name="Energy")]

    @classmethod
    def required_field_overrides(cls):
        required_list = super(GreenPowerProject, cls).required_field_overrides()
        required_list.append('description')
        return required_list

    @classmethod
    def required_metadata(cls):
        return {
            'image': {'max': 5, 'min': 0},  # optional, up to 5
            'file': {'max': 3, 'min': 0},  # optional, up to 5
            'author': {'max': 5, 'min': 0},  # optional, up to 5 (project contact)
            'website': {'max': 5, 'min': 0},  # optional, up to 5
        }


class GreenPowerProjectIndex(BaseIndex):
    def get_model(self):
        return GreenPowerProject

