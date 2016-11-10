from __future__ import unicode_literals

from collections import OrderedDict
from logging import getLogger
from operator import or_

import django_filters as filters
from django import forms
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.db.models import Q
from django.utils.timezone import now

from ..content.models import CONTENT_TYPES, ContentType, Material
from ..metadata.models import Organization, ProgramType, SustainabilityTopic, \
    AcademicDiscipline, CourseMaterialType, PublicationMaterialType
from .localflavor import CA_PROVINCES, US_STATES
from .forms import LeanSelectMultiple

logger = getLogger(__name__)
ALL = (('', 'All'),)

"""
    @idea - build a cache mixin and have all filters use a get_choices method
"""


# =============================================================================
# Generic Filter
# =============================================================================

class SearchFilter(filters.CharFilter):

    def filter(self, queryset, value):
        if not value:
            return queryset

        # Remove any special characters
        # http://lucene.apache.org/core/3_4_0/queryparsersyntax.html#Escaping%20Special%20Characters
        esc_string = '+-&|!\(\){}[]^"~*?:\\\/'
        translation_table = dict.fromkeys(map(ord, esc_string), None)
        query = value.translate(translation_table)

        search_vector = SearchVector('title',
                                     'description',
                                     'authors_search_data',
                                     'files_search_data',
                                     'images_search_data')

        return (queryset.annotate(search=search_vector).
                filter(search=query.lower()))

        # query = Raw(query.lower())
        # result_ids = (SearchQuerySet().filter(content__contains=query)
        #                               .values_list('ct_pk', flat=True))
        # return queryset.filter(pk__in=result_ids).distinct()


class TopicFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):

        topic_choices = cache.get('topic_filter_choices')
        if not topic_choices:
            topic_choices = SustainabilityTopic.objects.values_list(
                'slug', 'name')
            cache.set(
                'topic_filter_choices',
                topic_choices,
                settings.CACHE_TTL_SHORT)

        kwargs.update({
            'choices': topic_choices,
            'label': 'Sustainability Topic',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(TopicFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(topics__slug__in=value)


class ContentTypesFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):

        ct_choices = cache.get('ct_filter_choices')
        if not ct_choices:
            ct_choices = [
                (j, k.content_type_label()) for j, k in CONTENT_TYPES.items()
            ]
            cache.set(
                'ct_filter_choices', ct_choices, settings.CACHE_TTL_SHORT)

        kwargs.update({
            'choices': ct_choices,
            'label': 'Content Type',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(ContentTypesFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(content_type__in=value)


class OrganizationFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        # @todo: do I really need to load all the organizations,
        # or can I just load the selected ones?

        organizations = cache.get('org_filter_choices')
        if not organizations:
            organizations = Organization.objects.values_list('pk', 'org_name')
            cache.set(
                'org_filter_choices', organizations, settings.CACHE_TTL_SHORT)

        kwargs.update({
            'choices': organizations,
            'label': 'Organization(s)',
            'widget': LeanSelectMultiple,
        })
        super(OrganizationFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(organizations__in=value)


class TagFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        # @todo: how to avoid loading this every time?
        # it would be nice if the choices could only be the selected values
        # although I guess this provides some degree of validation

        tag_list = cache.get('tag_filter_choices')
        if not tag_list:
            tag_choices = ContentType.keywords.tag_model.objects.distinct(
                'name')
            tag_choices = tag_choices.values_list('slug', 'name')
            tag_list = [(slug, name) for slug, name in tag_choices]
            cache.set('tag_filter_choices', tag_list, settings.CACHE_TTL_SHORT)

        kwargs.update({
            'choices': tag_list,
            'label': 'Tags(s)',
            'widget': LeanSelectMultiple,
        })
        super(TagFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):

        new_queryset = queryset
        for slug in value:
            new_queryset = new_queryset.filter(keywords__slug=slug)
        return new_queryset


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

    def filter(self, queryset, value):
        if not value:
            return queryset

        # OPTIMIZE: this loads a big chunk of organizations just to use a
        # very little of them to filter the result queryset down.
        org_list = []
        for v in value:
            min, max = self.STUDENT_CHOICES_MAP[v][1]
            org_list += Organization.objects.in_fte_range(min, max)
        return queryset.filter(organizations__in=org_list).distinct()


class CountryFilter(filters.ChoiceFilter):
    def __init__(self, *args, **kwargs):

        countries = cache.get('country_filter_choices')
        if not countries:
            queryset = ContentType.objects.published().order_by(
                'organizations__country')
            queryset = queryset.values_list(
                'organizations__country_iso',
                'organizations__country').distinct()
            countries = ALL + tuple(
                [c for c in queryset if (c[0] is not None and c[0] is not '')])

            cache.set(
                'country_filter_choices', countries, settings.CACHE_TTL_SHORT)

        kwargs.update({
            'choices': countries,
            'label': 'Country/ies',
        })
        super(CountryFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(organizations__country_iso=value)


class BaseStateFilter(filters.ChoiceFilter):
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': self.get_choices(),
            'label': self.get_label(),
            'widget': forms.widgets.CheckboxSelectMultiple,
        })
        super(BaseStateFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(organizations__state__in=value)


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

        year_choices = cache.get('publish_year_filter_choices')
        if not year_choices:
            year_choices = self.get_choices()
            cache.set(
                'publish_year_filter_choices',
                year_choices,
                settings.CACHE_TTL_SHORT)

        kwargs.update({
            'choices': year_choices,
            'label': 'Year Posted',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(PublishedFilter, self).__init__(*args, **kwargs)

    def get_choices(self):

        queryset = ContentType.objects.published()

        # Find the minimum and maximum year of all ct's and put them
        # in a range for choices.
        # @todo - add caching here for performance
        min_year = queryset.order_by('published').first()
        max_year = queryset.order_by('-published').first()

        if not min_year or not max_year:
            year_choices = ((now().year, now().year),)
        elif min_year.published.year == max_year.published.year:
            year_choices = (
                (min_year.published.year, min_year.published.year),
            )
        else:
            year_choices = [(i, i) for i in range(
                min_year.published.year, max_year.published.year + 1)]

        return year_choices

    def filter(self, queryset, value):
        if not value:
            return queryset
        query = reduce(or_, (Q(published__year=x) for x in value))
        return queryset.filter(query)


class OrderingFilter(filters.ChoiceFilter):
    field_class = forms.fields.ChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': (
                ('title', 'Title'),
                ('content_type', 'Content Type'),
                ('-published', 'Date Posted'),
                ('-date_created', "Date Created, Published, Presented")
            ),
            'label': 'Sort by:',
            'widget': forms.widgets.RadioSelect,
        })
        super(OrderingFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        if not value:
            return queryset.order_by('-published')
        return queryset.order_by(value)


# Academic Program specific
class ProgramTypeFilter(filters.ChoiceFilter):
    """
    Academic Program specific Program Type filter.
    """
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):

        program_choices = cache.get('program_type_filter_choices')
        if not program_choices:
            program_choices = ProgramType.objects.values_list('pk', 'name')
            cache.set(
                'program_type_filter_choices',
                program_choices,
                settings.CACHE_TTL_SHORT)

        kwargs.update({
            'choices': program_choices,
            'label': 'Program Type',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(ProgramTypeFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        """
        Filters always work against the base `ContenType` model, not it's
        sub classes. We have to do a little detour to match them up.
        """
        if not value:
            return queryset
        from ..content.types.academic import AcademicProgram
        return queryset.filter(pk__in=AcademicProgram.objects.filter(
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

    def filter(self, queryset, value):
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
                return queryset.filter(Q(**cc_kwargs) | Q(**t_kwargs))
            elif selected_cc_values:
                return queryset.filter(**cc_kwargs)
            else:
                return queryset.filter(**t_kwargs)

        return queryset


class MaterialTypeFilter(filters.ChoiceFilter):
    """
    Filter a course Material by type
    """
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):

        kwargs.update({
            'choices': CourseMaterialType.objects.values_list('pk', 'name'),
            'label': 'Material Type',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(MaterialTypeFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        if value:
            return queryset.filter(pk__in=Material.objects.filter(
                material_type__in=value).values_list('pk', flat=True))
        return queryset


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

    def filter(self, queryset, value):
        if value:
            return queryset.filter(pk__in=Material.objects.filter(
                course_level__in=value).values_list('pk', flat=True))
        return queryset


# Publication specific
class PublicationTypeFilter(filters.ChoiceFilter):
    """
    Publication specific Type filter.
    """
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'choices': PublicationMaterialType.objects.all().values_list(),
            'label': 'Publication Type',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(PublicationTypeFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        """
        Filters always work against the base `ContenType` model, not it's
        sub classes. We have to do a little detour to match them up.
        """
        if not value:
            return queryset
        from ..content.types.publications import Publication
        return queryset.filter(pk__in=Publication.objects.filter(
            material_type__in=value).values_list('pk', flat=True))


class CreatedFilter(filters.ChoiceFilter):
    """
        This filter takes an optional argument of ContentTypeClass which allows
        us to show only the years that have values.
    """

    field_class = forms.fields.MultipleChoiceField

    def __init__(self, ContentTypeClass=ContentType, *args, **kwargs):

        year_choices = cache.get('created_year_filter_choices')
        if not year_choices:
            year_choices = self.get_choices(ContentTypeClass)
            cache.set(
                'created_year_filter_choices',
                year_choices,
                settings.CACHE_TTL_SHORT)

        kwargs.update({
            'choices': year_choices,
            'label': 'Year created, published, or presented',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(CreatedFilter, self).__init__(*args, **kwargs)

    def get_choices(self, ContentTypeClass):

        queryset = ContentTypeClass.objects.published().filter(
            date_created__isnull=False)
        queryset = queryset.order_by('-date_created')

        # Find the minimum and maximum year of all ct's and put them
        # in a range for choices.
        # @todo - add caching here for performance
        all_dates = queryset.values_list('date_created', flat=True)
        if all_dates:
            # using set to remove duplicates
            distinct_years = list(set([d.year for d in all_dates]))
            distinct_years.sort(reverse=True)
            year_choices = [(i, i) for i in distinct_years]
        else:
            year_choices = ((now().year, now().year),)

        return year_choices

    def filter(self, queryset, value):
        if not value:
            return queryset
        query = reduce(or_, (Q(date_created__year=x) for x in value))
        return queryset.filter(query)


class DisciplineFilter(filters.ChoiceFilter):
    """
    Academic Discipline Filter
    """
    field_class = forms.fields.MultipleChoiceField

    def __init__(self, *args, **kwargs):

        discipline_choices = cache.get('academic_discipline_filter_choices')
        if not discipline_choices:
            discipline_choices = AcademicDiscipline.objects.values_list(
                'pk', 'name')
            cache.set(
                'academic_discipline_filter_choices',
                discipline_choices,
                settings.CACHE_TTL_SHORT)

        kwargs.update({
            'choices': discipline_choices,
            'label': 'Academic Discipline',
            'widget': forms.widgets.CheckboxSelectMultiple(),
        })
        super(DisciplineFilter, self).__init__(*args, **kwargs)

    def filter(self, queryset, value):
        if not value:
            return queryset
        return queryset.filter(disciplines__in=value)
