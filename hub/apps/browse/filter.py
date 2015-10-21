from collections import OrderedDict

import django_filters as filters
from django import forms

from ..content.models import CONTENT_TYPE_CHOICES, ContentType
from ..metadata.models import Organization, SustainabilityTopic, ProgramType

#==============================================================================
# Generic Filter
#==============================================================================

class SearchFilter(filters.CharFilter):
    """
    Search currently searches the title against the given keyword.

    TODO: Implement search engine
    """
    def filter(self, qs, value):
        return qs.filter(title__icontains=value)


class TopicFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': SustainabilityTopic.objects.values_list('slug', 'name'),
            'label': 'Sustainability Topic',
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
            'choices': CONTENT_TYPE_CHOICES,
            'label': 'Content Type',
        })
        super(ContentTypesFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(content_type__in=value)

class StudentFteFilter(filters.ChoiceFilter):
    STUDENT_CHOICES_MAP = OrderedDict([
        # {name: (label, min/max)}
        ('', ('All', (None, None))),
        ('lt_5000', ('<5000', (None, 5000))),
        ('5k_10k', ('5000-10,000', (5000, 10000))),
        ('10k_20k', ('10,000-20,000', (10000, 20000))),
        ('gt_20k', ('>20,000', (20000, None))),
    ])

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': [(i[0], i[1][0]) for i in self.STUDENT_CHOICES_MAP.items()],
            'label': 'Institution Size',
        })
        super(StudentFteFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        min, max = self.STUDENT_CHOICES_MAP[value][1]
        org_list = Organization.objects.in_fte_range(min, max)
        return qs.filter(organizations__in=org_list).distinct()


class CountryFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        countries = (Organization.objects
            .exclude(country='')
            .order_by('country')
            .values_list('country', 'country')
            .distinct())

        kwargs.update({
            'choices': countries,
            'label': 'Country',
        })
        super(CountryFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(organizations__country=value)


class GenericFilterSet(filters.FilterSet):
    """
    The genric Filter form handling the filtering for all views: search, content
    types and sustainability topic. The browse view might extend the list of
    filters dynamically per content type, using above   `CONTENT_TYPE_FILTERS`
    mapping.
    """
    search = SearchFilter()
    topics = TopicFilter()
    content_type = ContentTypesFilter()
    organizations = filters.MultipleChoiceFilter
    size = StudentFteFilter()
    published = filters.DateRangeFilter()
    country = CountryFilter()
    state = filters.ChoiceFilter()

    class Meta:
        model = ContentType
        fields = []  # Don't set any automatic fields, we already defined
                     # a specific list above.

#==============================================================================
# Academic Program
#==============================================================================

class ProgramTypeFilter(filters.ChoiceFilter):
    """
    Academic Program specific Program Type filter.
    """
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': ProgramType.objects.values_list('pk', 'name'),
            'label': 'Program Type',
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


class AcademicBrowseFilter(GenericFilterSet):
    program_type = ProgramTypeFilter()
