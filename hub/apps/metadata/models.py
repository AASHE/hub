from __future__ import unicode_literals

from logging import getLogger

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.conf import settings

import feedparser
from model_utils.models import TimeStampedModel
from iss.models import Organization as ISSOrganization

logger = getLogger(__name__)


@python_2_unicode_compatible
class MetadataBaseModel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SustainabilityTopic(MetadataBaseModel):
    color = models.CharField('HEX Color', max_length=7, default='#ff0000')
    slug = models.SlugField()
    introduction = models.TextField(blank=True, null=True)
    rss_feed = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    icon = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        ordering = ('order', 'name')
        verbose_name = 'Sustainability Topic'
        verbose_name_plural = 'Sustainability Topics'

    def get_absolute_url(self):
        return reverse('browse:browse', kwargs={'topic': self.slug})

    def get_rss_items(self):
        """
        Fetch, parse and cache rss items
        """
        if not self.rss_feed:
            return None

        CACHE_KEY = 'TOPIC_FEED_ITEMS_{}'.format(self.slug.upper())

        entries = cache.get(CACHE_KEY)

        if entries:
            return entries

        try:
            feed = feedparser.parse(self.rss_feed)
        except Exception as e: # Any error is bad here, catch all.
            logger.error('Feed parse failed; {}'.format(self.rss_feed))
            logger.exception(e)
            return None

        entries = feed.entries[:20]
        cache.set(CACHE_KEY, entries, settings.CACHE_TTL_LONG)
        return entries


@python_2_unicode_compatible
class SustainabilityTopicFavorite(TimeStampedModel):
    topic = models.ForeignKey(SustainabilityTopic, verbose_name='Sustainability Topic')
    ct = models.ForeignKey('content.ContentType', verbose_name='Content Type')

    def __str__(self):
        return '{} in {}'.format(self.ct, self.topic)


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
