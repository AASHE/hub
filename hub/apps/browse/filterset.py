from .filter import *
from collections import OrderedDict
from ..content.types.green_power_projects import GreenPowerProject


class GenericFilterSet(filters.FilterSet):
    """
    The genric Filter form handling the filtering for all views: search,
    content types and sustainability topic. The browse view might extend the
    list of filters dynamically per content type, using above
    `CONTENT_TYPE_FILTERS` mapping.
    """
    search = SearchFilter(widget=forms.HiddenInput)
    gallery_view = GalleryFilter()
    content_type = ContentTypesFilter()
    topics = TopicFilter()
    discipline = DisciplineFilter()
    institutional_office = InstitutionalOfficeFilter()
    tagfilter = TagFilter('tags')
    organizations = OrganizationFilter()
    institution_types = InstitutionTypeFilter()
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


class ExlcudeGalleryFilterMixin(object):
    """
        removes the gallery filter from a filterset
        in the absence of a better approach coming to me, I had to create a
        new OrderedDict to make this work...
        probably not the most efficient way, but all I could come up with

        setting `gallery_view = None` on the child Filterset didn't work
    """
    def __init__(self, *args, **kwargs):
        super(ExlcudeGalleryFilterMixin, self).__init__(*args, **kwargs)

        # add the gallery filter to the top of the filters list
        od = OrderedDict()
        for key in self.filters:
            if key is not 'gallery_view':
                od[key] = self.filters[key]
        self.filters = od


##############################################################################
# All Content Types get their own filterset
##############################################################################


class AcademicBrowseFilterSet(ExlcudeGalleryFilterMixin, GenericFilterSet):
    program_type = ProgramTypeFilter()
    from ..content.types.academic import AcademicProgram
    created = CreatedFilter(AcademicProgram)


class CaseStudyBrowseFilterSet(GenericFilterSet):
    from ..content.types.casestudies import CaseStudy
    created = CreatedFilter(CaseStudy)


class CenterAndInstituteBrowseFilterSet(ExlcudeGalleryFilterMixin,
                                        GenericFilterSet):
    from ..content.types.centers import CenterAndInstitute
    created = CreatedFilter(CenterAndInstitute)


class GreenPowerBrowseFilterSet(filters.FilterSet):
    search = SearchFilter(widget=forms.HiddenInput)
    gallery_view = GalleryFilter()
    content_type = ContentTypesFilter()
    topics = TopicFilter()
    discipline = DisciplineFilter()
    institutional_office = InstitutionalOfficeFilter()
    tagfilter = TagFilter('tags')
    organizations = OrganizationFilter()
    institution_types = InstitutionTypeFilter()
    size = StudentFteFilter()
    country = CountryFilter(required=False)
    state = StateFilter(required=False)
    province = ProvinceFilter(required=False)
    published = PublishedFilter()
    created = CreatedFilter()
    installation = GreenPowerInstallationFilter()
    ownership = GreenPowerOwnershipFilter()
    project_size = GreenPowerProjectSizeFilter()
    created = CreatedFilter(GreenPowerProject)
    order = GreenPowerOrderingFilter()

    class Meta:
        model = ContentType
        #  Don't set any automatic fields, we already defined
        # a specific list above.
        fields = []

class MaterialBrowseFilterSet(ExlcudeGalleryFilterMixin, GenericFilterSet):
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
    conference_name = ConferenceNameFilter()
    from ..content.types.presentations import Presentation
    created = CreatedFilter(Presentation)


class PublicationBrowseFilterSet(GenericFilterSet):
    publication_type = PublicationTypeFilter()
    from ..content.types.publications import Publication
    created = CreatedFilter(Publication)


class ToolBrowseFilterSet(ExlcudeGalleryFilterMixin, GenericFilterSet):
    from ..content.types.tools import Tool
    created = CreatedFilter(Tool)


class VideoBrowseFilterSet(ExlcudeGalleryFilterMixin, GenericFilterSet):
    from ..content.types.videos import Video
    created = CreatedFilter(Video)
