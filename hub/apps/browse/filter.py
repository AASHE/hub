from collections import OrderedDict

import django_filters as filters
from django import forms

from ..content.models import ContentType, CONTENT_TYPE_CHOICES
from ..metadata.models import Organization, ProgramType, SustainabilityTopic


class ProgramTypeFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': ProgramType.objects.values_list('pk', 'name'),
            'label': 'Program Type',
        })
        super(ProgramTypeFilter, self).__init__(*args, **kwargs)


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
        return qs.filter(organizations__in=org_list)


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
