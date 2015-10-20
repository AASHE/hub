import django_filters as filters

from .filter import *


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


class AcademicBrowseFilter(GenericFilterSet):
    program_type = ProgramTypeFilter()
