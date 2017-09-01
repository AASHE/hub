from django.db import models
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
        ('< 3', '< 3'),
        ('4 - 4.9', '4 - 4.9'),
        ('5 - 5.9', '5 - 5.9'),
        ('6 - 6.9', '6 - 6.9'),
        ('7 - 7.9', '7 - 7.9'),
        ('8 - 8.9', '8 - 8.9'),
        ('9 - 9.9', '9 - 9.9'),
        ('10 - 10.9', '10 - 10.9'),
        ('11 - 11.9', '11 - 11.9'),
        ('> 12', '> 12'),
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

    project_size = models.PositiveIntegerField()
    annual_production = models.PositiveIntegerField(blank=True, null=True)
    installed_cost = models.PositiveIntegerField(blank=True, null=True)
    date_installed = models.DateField(blank=True, null=True)
    ownership_type = models.CharField(max_length=200, choices=OWNERSHIP_TYPES)
    installations = models.ManyToManyField(
        'metadata.GreenPowerInstallation',
        verbose_name='Green Power Installation',
        help_text='Select up to three'
    )
    finance_sources = models.ManyToManyField(
        'metadata.GreenPowerFinancing',
        verbose_name='Green Power Finanance Source',
        help_text='Select up to 3'
    )
    locations = models.ManyToManyField(
        'metadata.GreenPowerLocation',
        verbose_name='Green Power Location',
        help_text='Select up to 2'
    )
    money_saver = models.CharField(max_length=100, choices=MONEY_SAVER_OPTIONS)
    cost_savings_desc = models.TextField(blank=True, null=True)
    starting_ppa_price = models.CharField(blank=True, null=True, max_length=50, choices=PPA_CHOICES)
    ppa_escalator = models.CharField(blank=True, null=True, max_length=50, choices=PPA_CHOICES)
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
        return ['topics', 'disciplines']

    @classmethod
    def preset_topics(cls):
        return ['Energy']

    @classmethod
    def label_overrides(cls):
        return {
            'description': 'Description / Project Overview',
            'project_size': 'Project size (kW)'
        }

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

