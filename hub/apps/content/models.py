from __future__ import unicode_literals

from logging import getLogger

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from model_utils import Choices

from hub.permissions import get_aashe_member_flag
from .types.strings import AFFIRMATION

logger = getLogger(__name__)


class ContentTypeManager(models.Manager):
    def published(self):
        return self.filter(status=self.model.STATUS_CHOICES.published)


@python_2_unicode_compatible
class ContentType(TimeStampedModel):
    """
    The base Content Type model, each content type such as Publications or
    Images will have a one2one relation to this one. This model keeps all
    fields shares across content types.

    Additionally it keeps a choice field `content_type` which holds the name of
    the related content type.
    """
    STATUS_CHOICES = Choices(
        ('new', 'New'),
        ('published', 'Published'),
    )

    PERMISSION_CHOICES = Choices(
        ('open', 'Open - No login Required'),
        ('login', 'Public - Login Required'),
        ('member', 'Member - AASHE Member Status Required'),
    )

    content_type = models.CharField(max_length=40)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES.new)
    permission = models.CharField(max_length=20, choices=PERMISSION_CHOICES, default=PERMISSION_CHOICES.member)
    published = models.DateTimeField(blank=True, null=True)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    organizations = models.ManyToManyField('metadata.Organization', blank=True, verbose_name='Organizations')
    topics = models.ManyToManyField('metadata.SustainabilityTopic', blank=True, verbose_name='Sustainability Topics')
    disciplines = models.ManyToManyField('metadata.AcademicDiscipline', blank=True, verbose_name='Academic Disciplines')

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Genric Content Type'
        verbose_name_plural = '- All Content Types -'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Save the key value of the current ContentType Sub class (!) along
        # self.content_type so we know which instance belongs to the actual
        # base ContentType instance. Kinda funky dict-find-by-value here.
        self.content_type = CONTENT_TYPES.keys()[
            CONTENT_TYPES.values().index(self.__class__)]

        # Update the `published` date the first time this instance was set to
        # published.
        if not self.published and self.status == self.STATUS_CHOICES.published:
            self.published = timezone.now()

        return super(ContentType, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('browse:view', kwargs={'ct': self.content_type,
            'id': self.pk})

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

    def permission_flag(self, user):
        """
        Returns a corresponding "Login Required" or "Member required"
        flag based on the object permission and the given user.
        """
        # Open Document has no flag
        if self.permission == self.PERMISSION_CHOICES.open:
            return None

        # If the user is logged in, and the member permission is met,
        # all fine, no label.
        if user.is_authenticated():
            is_aashe_member = get_aashe_member_flag(user)
            if (self.permission == self.PERMISSION_CHOICES.member and
            not is_aashe_member):
                return 'member-required'
            else:
                return None

        # We know the user is not logged in, so give a proper label, either
        # member or just login required.
        if self.permission == self.PERMISSION_CHOICES.member:
            return 'member-required'
        return 'login-required'


@python_2_unicode_compatible
class Author(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="authors")
    is_author = models.BooleanField("I am an author", default=False)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    organization = models.ForeignKey('metadata.Organization', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Website(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="websites")
    label = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.label or 'Website object'


@python_2_unicode_compatible
class File(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="files")
    label = models.CharField(max_length=100, blank=True, null=True)
    item = models.FileField(help_text="The following files formats are "
        "aceptable: PDF, Excel, Word, PPT...", blank=True, null=True)
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Additional File'
        verbose_name_plural = 'Additional Files'

    def __str__(self):
        return self.label or 'File object'


@python_2_unicode_compatible
class Image(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="images")
    caption = models.CharField(max_length=500, blank=True, null=True)
    credit = models.CharField(max_length=500, blank=True, null=True)
    image = models.ImageField(help_text="The following files formats are "
        "acceptable: JPEG, PNG, TIFF...")
    affirmation = models.BooleanField('Affirmation of Ownership', default=False,
        help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Additional Image'
        verbose_name_plural = 'Additional Images'

    def __str__(self):
        return self.caption or 'Image object'

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
    *[(j, k._meta.verbose_name) for j, k in sorted(CONTENT_TYPES.items())]
)
