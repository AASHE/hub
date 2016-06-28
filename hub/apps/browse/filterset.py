from .filter import *


class GenericFilterSet(filters.FilterSet):
    """
    The genric Filter form handling the filtering for all views: search,
    content types and sustainability topic. The browse view might extend the
    list of filters dynamically per content type, using above
    `CONTENT_TYPE_FILTERS` mapping.
    """
    search = SearchFilter(widget=forms.HiddenInput)
    content_type = ContentTypesFilter()
    topics = TopicFilter()
    discipline = DisciplineFilter()
    tagfilter = TagFilter('tags')
    organizations = OrganizationFilter()
    organization_type = OrgTypeFilter()
    size = StudentFteFilter()
    country = CountryFilter(required=False)
    state = StateFilter(required=False)
    province = ProvinceFilter(required=False)
    published = PublishedFilter()
    created = CreatedFilter()
    order = OrderingFilter()

    class Meta:
        model = ContentType
        #  Don't set any automatic fields, we already defined
        # a specific list above.
        fields = []

##############################################################################
# All Content Types get their own filterset
##############################################################################

class AcademicBrowseFilterSet(GenericFilterSet):
    program_type = ProgramTypeFilter()
    from ..content.types.academic import AcademicProgram
    created = CreatedFilter(AcademicProgram)


class CaseStudyBrowseFilterSet(GenericFilterSet):
    from ..content.types.casestudies import CaseStudy
    created = CreatedFilter(CaseStudy)


class CenterAndInstituteBrowseFilterSet(GenericFilterSet):
    from ..content.types.centers import CenterAndInstitute
    created = CreatedFilter(CenterAndInstitute)


class CaseStudyBrowseFilterSet(GenericFilterSet):
    from ..content.types.courses import Material
    created = CreatedFilter(Material)


class MaterialBrowseFilterSet(GenericFilterSet):
    material_type = MaterialTypeFilter()
    course_level = CourseLevelFilter()
    from ..content.types.courses import Material
    created = CreatedFilter(Material)


class OutreachBrowseFilterSet(GenericFilterSet):
    from ..content.types.outreach import OutreachMaterial
    created = CreatedFilter(OutreachMaterial)


class PhotographBrowseFilterSet(GenericFilterSet):
    from ..content.types.photographs import Photograph
    created = CreatedFilter(Photograph)


class PresentationBrowseFilterSet(GenericFilterSet):
    from ..content.types.presentations import Presentation
    created = CreatedFilter(Presentation)


class PublicationBrowseFilterSet(GenericFilterSet):
    publication_type = PublicationTypeFilter()
    from ..content.types.publications import Publication
    created = CreatedFilter(Publication)


class ToolBrowseFilterSet(GenericFilterSet):
    from ..content.types.tools import Tool
    created = CreatedFilter(Tool)


class VideoBrowseFilterSet(GenericFilterSet):
    from ..content.types.videos import Video
    created = CreatedFilter(Video)
