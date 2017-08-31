from django.db import models
from ..models import ContentType, ContentTypeManager
from ..search import BaseIndex


class GreenPowerProject(ContentType):

    INSTALLATION_TYPES = (
        ('solar-canopy', 'Solar - Canopy'),
        ('solar-rooftop', 'Solar - Roof Top Mount'),
        ('solar-wall', 'Solar - Wall Mount'),
        ('solar-ground-pole', 'Solar - Ground or Pole Mount'),
        ('solar-building-photovoltaic', 'Solar - Building Integrated Photovoltaic'),
        ('solar-other', 'Solar - Other'),
        ('wind-horizontal', 'Wind - Horizontal Axis'),
        ('wind-horizontal', 'Wind - Vertical Axis'),
        ('hydroelectric', 'Low - Impact Hydroelectric'),
    )

    OWNERSHIP_TYPES = (
        ('unknown', 'Unknown'),
        ('institution-owned', 'Institution Owned'),
        ('third-party-lease', 'Third-party owned (lease)'),
        ('third-party-purchase', 'Third-party owned (power purchase agreement)'),
    )

    project_size = models.PositiveIntegerField()
    annual_production = models.PositiveIntegerField(blank=True, null=True)
    installed_cost = models.PositiveIntegerField(blank=True, null=True)
    date_installed = models.DateField(blank=True, null=True)
    first_installation_type = models.CharField(max_length=200, choices=INSTALLATION_TYPES)
    second_installation_type = models.CharField(max_length=200, choices=INSTALLATION_TYPES)
    third_installation_type = models.CharField(max_length=200, choices=INSTALLATION_TYPES)
    ownership_type = models.CharField(max_length=200, choices=OWNERSHIP_TYPES)

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
    def label_overrides(cls):
        return {
            'description': 'Description / Project Overview',
            'date_'
        }

    @classmethod
    def required_field_overrides(cls):
        required_list = super(GreenPowerProject, cls).required_field_overrides()
        required_list.append('description')
        return required_list

    # @classmethod
    # def required_metadata(cls):
    #     return {
    #         'image': {'max': 5, 'min': 0},  # optional, up to 5
    #         'file': {'max': 3, 'min': 0},  # optional, up to 5
    #         'author': {'max': 5, 'min': 1},  # required, up to 5
    #         'website': {'max': 5, 'min': 0},  # optional, up to 5
    #     }


class GreenPowerProjectIndex(BaseIndex):
    def get_model(self):
        return GreenPowerProject

