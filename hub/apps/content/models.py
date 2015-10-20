from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
from model_utils import Choices


@python_2_unicode_compatible
class ContentType(TimeStampedModel):
    """
    The base Content Type model, each content type such as Publications or
    Images will have a one2one relation to this one. This model keeps all
    fields shares across content types.

    Additionally it keeps a choice field `content_type` which holds the name of
    the related content type.
    """
    # List of available content type models. Left side is the lowercase (!)
    # modelname of each subclassed content type which we use to link there
    # within the admin.
    content_type = models.CharField(max_length=40)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    organizations = models.ManyToManyField('metadata.Organization', blank=True, verbose_name='Organizations')
    topics = models.ManyToManyField('metadata.SustainabilityTopic', blank=True, verbose_name='Sustainability Topics')
    disciplines = models.ManyToManyField('metadata.AcademicDiscipline', blank=True, verbose_name='Academic Disciplines')

    class Meta:
        verbose_name = 'Genric Content Type'
        verbose_name_plural = '- All Content Types -'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Save the key value of the current ContentType Sub class (!) along
        self.content_type so we know which instance belongs to the actual
        base ContentType instance.
        """
        # Kinda funky dict-find-by-value
        self.content_type = CONTENT_TYPES.keys()[
            CONTENT_TYPES.values().index(self.__class__)
        ]
        return super(ContentType, self).save(*args, **kwargs)

    @property
    def content_type_label(self):
        """
        The `verbose_name` of the attached content type subclass of this
        main content type object.
        """
        return CONTENT_TYPE_CHOICES[self.content_type]

    @property
    def title_label(self):
        """
        Content types all share the same `title` field, however it's label might
        be different. 'Title' or 'Presentation Title'. Here you can override it
        per content type.
        """
        return 'Title'

    @classmethod
    def custom_filterset(self):
        """
        Each content type sub class may define a custom filter with their
        additional fields here. If not set, the views will use the generic
        FilterSet.
        """
        return None


@python_2_unicode_compatible
class Author(TimeStampedModel):
    ct = models.ForeignKey(ContentType)
    is_author = models.BooleanField("I am an author", default=False)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    organization = models.ForeignKey('metadata.Organization', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Website(TimeStampedModel):
    ct = models.ForeignKey(ContentType)
    label = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class File(TimeStampedModel):
    ct = models.ForeignKey(ContentType)
    label = models.CharField(max_length=100, blank=True, null=True)
    item = models.FileField(help_text="The following files formats are "
        "aceptable: PDF, Excel, Word, PPT...", blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False)

    class Meta:
        verbose_name = 'Additional File'
        verbose_name_plural = 'Additional Files'

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Image(TimeStampedModel):
    ct = models.ForeignKey(ContentType)
    caption = models.CharField(max_length=500, blank=True, null=True)
    credit = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(help_text="The following files formats are "
        "acceptable: JPEG, PNG, TIFF...")

    class Meta:
        verbose_name = 'Additional Image'
        verbose_name_plural = 'Additional Images'

    def __str__(self):
        return self.caption

#==============================================================================
# Mapping of all available content types.
#
# We also load the content types here into the models namespace, so they are
# registered in the system, and the migration.
#==============================================================================
from .types.academic import AcademicProgram
from .types.casestudies import CaseStudy
from .types.centers import CenterAndInstitute
from .types.courses import Material
from .types.outreach import OutreachMaterial
from .types.photographs import Photograph
from .types.presentations import Presentation
from .types.publications import Publication
from .types.tools import Tool
from .types.videos import Video

CONTENT_TYPES = {
    'academicprogram': AcademicProgram,
    'casestudy': CaseStudy,
    'center': CenterAndInstitute,
    'material': Material,
    'outreach': OutreachMaterial,
    'photograph': Photograph,
    'presentation': Presentation,
    'publication': Publication,
    'tool': Tool,
    'video': Video,
}

# Auto-generate a list of Choices for each Content type. It doesn't add too much
# magic, it just tries to get the Content type Name out of `meta.verbose_name`,
# otherwise it tries to auto-generate the name.
CONTENT_TYPE_CHOICES = Choices(
    *[(j, k._meta.verbose_name) for j, k in CONTENT_TYPES.items()]
)
