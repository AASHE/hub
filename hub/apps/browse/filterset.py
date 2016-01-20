from .filter import *


class GenericFilterSet(filters.FilterSet):
    """
    The genric Filter form handling the filtering for all views: search,
    content types and sustainability topic. The browse view might extend the
    list of filters dynamically per content type, using above
    `CONTENT_TYPE_FILTERS` mapping.
    """
    search = SearchFilter(widget=forms.HiddenInput)
    topics = TopicFilter()
    content_type = ContentTypesFilter()
    organizations = OrganizationFilter()
    organization_type = OrgTypeFilter()
    size = StudentFteFilter()
    published = PublishedFilter()
    country = CountryFilter(required=False)
    state = StateFilter(required=False)
    order = OrderingFilter()

    class Meta:
        model = ContentType
        #  Don't set any automatic fields, we already defined
        # a specific list above.
        fields = []


class AcademicBrowseFilterSet(GenericFilterSet):
    program_type = ProgramTypeFilter()


class MaterialBrowseFilterSet(GenericFilterSet):
    material_type = MaterialTypeFilter()
    course_level = CourseLevelFilter()
