from __future__ import unicode_literals

from collections import OrderedDict
from logging import getLogger
from operator import or_

import django_filters as filters
from django import forms
from django.db.models import Q

from haystack.inputs import Raw
from haystack.query import SearchQuerySet

from ..content.models import CONTENT_TYPES, ContentType
from ..metadata.models import Organization, ProgramType, SustainabilityTopic
from .localflavor import CA_PROVINCES, US_STATES
from .forms import LeanSelectMultiple

logger = getLogger(__name__)
ALL = (('', 'All'),)


#==============================================================================
# Generic Filter
#==============================================================================

class SearchFilter(filters.CharFilter):
    """
    Search currently searches the title against the given keyword.

    TODO: Implement search engine
    """
    def filter(self, qs, value):
        if not value:
            return qs

        query = Raw(value.lower())
        result_ids = (SearchQuerySet().filter(content__contains=query)
                                      .values_list('ct_pk', flat=True))
        return qs.filter(pk__in=result_ids).distinct()


class TopicFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': SustainabilityTopic.objects.values_list('slug', 'name'),
            'label': 'Sustainability Topic',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(TopicFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(topics__slug__in=value)


class ContentTypesFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': [(j, k.content_type_label()) for j, k in CONTENT_TYPES.items()],
            'label': 'Content Type',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(ContentTypesFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(content_type__in=value)



class OrganizationFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        organizations = Organization.objects.values_list('pk', 'org_name')
        kwargs.update({
            'choices': organizations,
            'label': 'Organization',
            'widget': LeanSelectMultiple,
        })
        super(OrganizationFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(organizations__in=value)


class StudentFteFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField
    STUDENT_CHOICES_MAP = OrderedDict([
        # {name: (label, min/max)}
        ('lt_5000', ('<5000', (None, 5000))),
        ('5k_10k', ('5000-10,000', (5000, 10000))),
        ('10k_20k', ('10,000-20,000', (10000, 20000))),
        ('gt_20k', ('>20,000', (20000, None))),
    ])

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': [(i[0], i[1][0]) for i in self.STUDENT_CHOICES_MAP.items()],
            'label': 'Institution Size',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(StudentFteFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs

        # OPTIMIZE: this loads a big chunk of organizations just to use a
        # very little of them to filter the result queryset down.
        org_list = []
        for v in value:
            min, max = self.STUDENT_CHOICES_MAP[v][1]
            org_list += Organization.objects.in_fte_range(min, max)
        return qs.filter(organizations__in=org_list).distinct()


class CountryFilter(filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):
        countries = (Organization.objects.country_list())
        countries = ALL + tuple(countries)
        kwargs.update({
            'choices': countries,
            'label': 'Country',
        })
        super(CountryFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(organizations__country_iso=value)


class StateFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        states = (
            ('United States', US_STATES),
            ('Canada', CA_PROVINCES),
        )

        kwargs.update({
            'choices': states,
            'label': 'State',
            'widget': forms.widgets.CheckboxSelectMultiple,
        })
        super(StateFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(organizations__state__in=value)


class PublishedFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        # Find the minimum and maximum year of all topics and put them
        # in a range for choices.

        min_year = ContentType.objects.published().order_by('published').first()
        max_year = ContentType.objects.published().order_by('-published').first()

        if not min_year or not max_year:
            year_choices = ((2015, 2015),)
        elif min_year.published.year == max_year.published.year:
            year_choices = ((min_year.published.year, min_year.published.year),)
        else:
            year_choices = [(i, i) for i in range(
                min_year.published.year, max_year.published.year)]

        kwargs.update({
            'choices': year_choices,
            'label': 'Published',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(PublishedFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        query = reduce(or_, (Q(published__year=x) for x in value))
        return qs.filter(query)


class OrderingFilter(filters.ChoiceFilter):
    field_class = forms.fields.ChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': (
                ('title', 'Title'),
                ('content_type', 'Content Type'),
                ('-published', 'Publish Date'),
            ),
            'label': 'Sort by',
            'widget': forms.widgets.RadioSelect,
        })
        super(OrderingFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.order_by(value)


# Academic Program specific
class ProgramTypeFilter(filters.ChoiceFilter):
    """
    Academic Program specific Program Type filter.
    """
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': ProgramType.objects.values_list('pk', 'name'),
            'label': 'Program Type',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(ProgramTypeFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        """
        Filters always work against the base `ContenType` model, not it's
        sub classes. We have to do a little detour to match them up.
        """
        if not value:
            return qs
        from ..content.types.academic import AcademicProgram
        return qs.filter(pk__in=AcademicProgram.objects.filter(
            program_type__in=value).values_list('pk', flat=True))
