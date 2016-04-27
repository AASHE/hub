from __future__ import unicode_literals

from collections import OrderedDict
from logging import getLogger
from operator import or_

import django_filters as filters
from django import forms
from django.db.models import Q
from django.utils.timezone import now

from haystack.inputs import Raw
from haystack.query import SearchQuerySet

from ..content.models import CONTENT_TYPES, ContentType, Material
from ..metadata.models import Organization, ProgramType, SustainabilityTopic
from .localflavor import CA_PROVINCES, US_STATES
from .forms import LeanSelectMultiple

logger = getLogger(__name__)
ALL = (('', 'All'),)


# =============================================================================
# Generic Filter
# =============================================================================

class SearchFilter(filters.CharFilter):
    """
    Search currently searches the title against the given keyword.

    TODO: Implement search engine
    """
    def filter(self, qs, value):
        if not value:
            return qs

        # Remove any special characters
        # http://lucene.apache.org/core/3_4_0/queryparsersyntax.html#Escaping%20Special%20Characters
        esc_string = '+-&|!\(\){}[]^"~*?:\\\/'
        translation_table = dict.fromkeys(map(ord, esc_string), None)
        query = value.translate(translation_table)
        
        query = Raw(query.lower())
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
            'choices': [
                (j, k.content_type_label()) for j, k in CONTENT_TYPES.items()
            ],
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
        # @todo: do I really need to load all the organizations,
        # or can I just load the selected ones?
        organizations = Organization.objects.values_list('pk', 'org_name')
        kwargs.update({
            'choices': organizations,
            'label': 'Organization(s)',
            'widget': LeanSelectMultiple,
        })
        super(OrganizationFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(organizations__in=value)


class TagFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        # @todo: how to avoid loading this every time?
        # it would be nice if the choices could only be the selected values
        # although I guess this provides some degree of validation
        tag_choices = ContentType.keywords.tag_model.objects.distinct('name')
        # tag_choices = tag_choices.filter(name__startswith="behav")
        tag_choices = tag_choices.values_list('slug', 'name')
        # import pdb; pdb.set_trace()
        
        kwargs.update({
            'choices': tag_choices,
            'label': 'Tags(s)',
            'widget': LeanSelectMultiple,
        })
        super(TagFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        
        new_qs = qs
        for slug in value:
            new_qs = new_qs.filter(keywords__slug=slug)
        return new_qs


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
            'choices': [
                (i[0], i[1][0]) for i in self.STUDENT_CHOICES_MAP.items()
            ],
            'label': 'Student FTE',
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
        # @WARNING: keep an eye on performance here.
        # We might want to use caching

        # countries = (Organization.objects.country_list())
        qs = ContentType.objects.published().order_by('organizations__country')
        qs = qs.values_list(
            'organizations__country_iso',
            'organizations__country').distinct()
        countries = ALL + tuple(
            [c for c in qs if (c[0] is not None and c[0] is not '')])
        kwargs.update({
            'choices': countries,
            'label': 'Country/ies',
        })
        super(CountryFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(organizations__country_iso=value)


class BaseStateFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': self.get_choices(),
            'label': self.get_label(),
            'widget': forms.widgets.CheckboxSelectMultiple,
        })
        super(BaseStateFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs
        return qs.filter(organizations__state__in=value)


class StateFilter(BaseStateFilter):

    def get_choices(self):
        return US_STATES

    def get_label(self):
        return 'State(s)'


class ProvinceFilter(BaseStateFilter):

    def get_choices(self):
        return CA_PROVINCES

    def get_label(self):
        return 'Province(s)'


class PublishedFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        # Find the minimum and maximum year of all topics and put them
        # in a range for choices.
        qs = ContentType.objects.published()

        min_year = qs.order_by('published').first()
        max_year = qs.order_by('-published').first()

        if not min_year or not max_year:
            year_choices = ((now().year, now().year),)
        elif min_year.published.year == max_year.published.year:
            year_choices = (
                (min_year.published.year, min_year.published.year),
            )
        else:
            year_choices = [(i, i) for i in range(
                min_year.published.year, max_year.published.year + 1)]

        kwargs.update({
            'choices': year_choices,
            'label': 'Year Posted',
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
                ('-published', 'Most Recent'),
            ),
            'label': 'Sort',
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


class OrgTypeFilter(filters.ChoiceFilter):
    """
    Filter on the organization type from the ISS
    """
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):

        self.carnegie_class_choices = [
            ("Associate", "Associate (2-year) Institution"),
            ("Baccalaureate", "Baccalaureate Institution"),
            ("Doctorate", "Doctoral/Research Institution"),
            ("Master", "Master's Institution"),
        ]

        self.type_choices = [
            ("Business", "Business"),
            ("System Office", "College or University System"),
            ("Government Agency", "Government Agency"),
            ("K-12 School", "K-12 School"),
            ("Nonprofit/NGO", "Non-profit/NGO"),
        ]

        kwargs.update({
            'choices': self.carnegie_class_choices + self.type_choices,
            'label': 'Organization Type',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(OrgTypeFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            cc_values = [x[0] for x in self.carnegie_class_choices]
            t_values = [x[0] for x in self.type_choices]
            selected_cc_values = []
            selected_t_values = []
            for v in value:
                # filter according to either carnegie or type
                try:
                    carnegie_index = cc_values.index(v)
                    selected_cc_values.append(v)
                except ValueError:
                    try:
                        type_index = t_values.index(v)
                        selected_t_values.append(v)
                    except ValueError:
                        pass

            cc_kwargs = {
                'organizations__carnegie_class__in': selected_cc_values}
            t_kwargs = {'organizations__org_type__in': selected_t_values}

            if selected_cc_values and selected_t_values:
                return qs.filter(Q(**cc_kwargs) | Q(**t_kwargs))
            elif selected_cc_values:
                return qs.filter(**cc_kwargs)
            else:
                return qs.filter(**t_kwargs)

        return qs


class MaterialTypeFilter(filters.ChoiceFilter):
    """
    Filter a course Material by type
    """
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):

        kwargs.update({
            'choices': Material.MATERIAL_TYPE_CHOICES,
            'label': 'Material Type',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(MaterialTypeFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            return qs.filter(pk__in=Material.objects.filter(
                material_type__in=value).values_list('pk', flat=True))
        return qs


class CourseLevelFilter(filters.ChoiceFilter):
    """
    Filter a course Material on level
    """
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):

        kwargs.update({
            'choices': Material.LEVEL_CHOICES,
            'label': 'Course Level',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(CourseLevelFilter, self).__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value:
            return qs.filter(pk__in=Material.objects.filter(
                course_level__in=value).values_list('pk', flat=True))
        return qs
