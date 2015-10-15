from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from iss.models import Organization as ISSOrganization


@python_2_unicode_compatible
class MetadataBaseModel(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SustainabilityTopic(MetadataBaseModel):
    color = models.CharField('HEX Color', max_length=7, default='#ff0000')
    slug = models.SlugField()

    class Meta:
        ordering = ('color', 'name',)
        verbose_name = 'Sustainability Topic'
        verbose_name_plural = 'Sustainability Topics'


class AcademicDiscipline(MetadataBaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Academic Discipline'
        verbose_name_plural = 'Academic Disciplines'


class InstitutionalOffice(MetadataBaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Institutional Office'
        verbose_name_plural = 'Institutional Offices'


class ProgramType(MetadataBaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Program Type'
        verbose_name_plural = 'Program Types'


class Country(MetadataBaseModel):
    class Meta:
        ordering = ('name',)
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'


class OrganizationManager(models.Manager):
    def country_list(self):
        """
        Returns a list of of Choices of all countries in the ISS organization
        database, **where the ISO code is set**. Some records don't have it set.
        """
        return (self.exclude(country_iso='')
                    .order_by('country')
                    .values_list('country_iso', 'country')
                    .distinct())

    def in_fte_range(self, min=None, max=None):
        """
        Returns all organizations within a given min/max enrollment range.
        """
        if min and max:
            return self.filter(
                enrollment_fte__gte=min,
                enrollment_fte__lte=max
            )
        elif min:
            return self.filter(enrollment_fte__gte=min)
        elif max:
            return self.filter(enrollment_fte__lte=max)


@python_2_unicode_compatible
class Organization(ISSOrganization):
    """
    Proxy model to extend the existing ISS model.
    """
    objects = OrganizationManager()

    class Meta:
        proxy = True

    def __str__(self):
        if self.state:
            return '{}, {}'.format(self.org_name, self.state)
        else:
            return self.org_name
