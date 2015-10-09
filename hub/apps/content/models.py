from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel
from model_utils import Choices

from issdjango.models import Organizations
from ..metadata.models import SustainabilityTopic, AcademicDiscipline


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
    CONTENT_TYPES = Choices(
        ('academicprogram', 'Academic Program'),
        ('casestudy', 'Case Study'),
        ('center', 'Research Center & Institute'),
        ('presentation', 'Conference Presentation'),
        ('publication', 'Publication'),
        ('photograph', 'Photograph'),
        ('course', 'Course Material'),
        ('tool', 'Tool'),
        ('video', 'Video'),
        ('outreach', 'Outreach Material'),
    )

    content_type = models.CharField(max_length=40, choices=CONTENT_TYPES)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    organizations = models.ManyToManyField(Organizations, blank=True, verbose_name='Organizations')
    topics = models.ManyToManyField(SustainabilityTopic, blank=True, verbose_name='Sustainability Topics')
    disciplines = models.ManyToManyField(AcademicDiscipline, blank=True, verbose_name='Academic Disciplines')

    class Meta:
        verbose_name = 'Genric Content Type'
        verbose_name_plural = '- All Content Types -'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.content_type = self.class_content_type
        return super(ContentType, self).save(*args, **kwargs)

    @property
    def title_label(self):
        """
        Content types all share the same `title` field, however it's label might
        be different. 'Title' or 'Presentation Title'. Here you can override it
        per content type.
        """
        return 'Title'

    @property
    def class_content_type(self):
        """
        Each sub class needs to override this method and return the appropriate
        content type from self.TYPE_CHOICES:

            return self.CONTENT_TYPES.academicprogram
        """
        raise NotImplementedError('Subclasses need to override and set')

    @property
    def all_organizations(self):
        return ', '.join(self.organizations.all())

    @property
    def all_topics(self):
        return ', '.join(self.topics.all())

@python_2_unicode_compatible
class Author(TimeStampedModel):
    ct = models.ForeignKey(ContentType)
    is_author = models.BooleanField("I am an author", default=False)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    organization = models.ForeignKey(Organizations, blank=True, null=True)
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
    _file = models.FileField(help_text="The following files formats are "
        "aceptable: PDF, Excel, Word, PPT...", blank=True, null=True)

    def __str__(self):
        return self.label


@python_2_unicode_compatible
class Image(TimeStampedModel):
    ct = models.ForeignKey(ContentType)
    caption = models.CharField(max_length=500, blank=True, null=True)
    credit = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(help_text="The following files formats are "
        "acceptable: JPEG, PNG, TIFF...")

    def __str__(self):
        return self.caption


from .types.academic import AcademicProgram
from .types.publications import Publication
