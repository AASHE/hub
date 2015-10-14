from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


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
