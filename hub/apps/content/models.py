from __future__ import unicode_literals

import os

from logging import getLogger
from collections import OrderedDict
import tagulous

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from model_utils import Choices, FieldTracker
from slugify import slugify

from .help import AFFIRMATION

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
        ('declined', 'Declined')
    )

    PERMISSION_CHOICES = Choices(
        ('open', 'Open - No login Required'),
        ('login', 'Public - Login Required'),
        ('member', 'Member - AASHE Member Status Required'),
    )

    content_type = models.CharField(max_length=40)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES.new)
    permission = models.CharField(
        max_length=20,
        choices=PERMISSION_CHOICES,
        default=PERMISSION_CHOICES.member)
    published = models.DateTimeField(
        blank=True,
        null=True,
        help_text='This timestamp is automatically set once the status becomes'
        ' "Published".')
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True)

    title = models.CharField(max_length=500)  # label set by self.title_label
    slug = models.CharField(max_length=500, editable=False)

    description = models.TextField('Description', blank=True, null=True)

    organizations = models.ManyToManyField(
        'metadata.Organization',
        blank=True,
        verbose_name='Organization(s)',
        help_text="""Select the institution(s) and/or organization(s) that are
        directly tied to this resource. If an organization is not on the
        dropdown list, please contact resources@aashe.org.""")

    topics = models.ManyToManyField(
        'metadata.SustainabilityTopic',
        verbose_name='Sustainability Topic(s)',
        help_text="""Select up to three topics that relate most closely to 
        this resource.""")

    disciplines = models.ManyToManyField(
        'metadata.AcademicDiscipline',
        verbose_name='Academic Discipline(s)',
        help_text="""Only include if an academic discipline is directly tied to
        this resource (select up to three).""",
        blank=True)

    institutions = models.ManyToManyField(
        'metadata.InstitutionalOffice',
        blank=True,
        verbose_name='Office(s) or Department(s)',
        help_text='''Only include if an office or division on campus is
        directly tied to this resource (select up to three).''')

    keywords = tagulous.models.TagField(
        verbose_name='Tags',
        blank=True,
        space_delimiter=False,
        help_text="""Enter keywords that will be helpful for grouping this
        resource (e.g. "bottled water" for bottled water initiatives). For
        multiple tags, use comma or return as separator.""")

    notes = models.TextField('Notes', blank=True, null=True, default='',
                             help_text="Internal notes.")

    status_tracker = FieldTracker(fields=['status'])

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

        # Update the slug value on first save. This doesn't need to be unique
        # since the actual db URL lookup is still done with the pk.
        if not self.slug:
            self.slug = slugify(self.title)

        return super(ContentType, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('browse:view', kwargs={'ct': self.content_type,
                                              'id': self.pk,
                                              'slug': self.slug})

    def get_admin_url(self):
        return reverse('admin:content_{0}_change'.format(self.content_type),
                       args=[self.pk])

    @classmethod
    def content_type_label(cls):
        """
        The `verbose_name` of the attached content type subclass of this
        main content type object.
        """
        return cls._meta.verbose_name_plural

    @property
    def instance_type_label(self):
        """
        The `verbose_name` of the attached content type subclass of this
        main content type object.
        """
        return CONTENT_TYPES[self.content_type]._meta.verbose_name_plural

    @classmethod
    def custom_filterset(self):
        """
        Each content type sub class may define a custom filter with their
        additional fields here. If not set, the views will use the generic
        FilterSet.
        """
        return None

    @classmethod
    def label_overrides(cls):
        """
        Each content type sub class may return a dictionary with

            <field name>: <label>

        overrides which is used later in the Submit form, to override the
        label of the respective field in the document form. Example:

            return {
                'title': 'Program Name',
                'description': 'Description or Abstract',
                'author': 'Presenter',
                'author_plural': 'Presenters',
            }
        """
        return {}

    @classmethod
    def required_field_overrides(cls):
        """
        Each content type subclass may return a list of field names
        which is used later in the Submit form to set the
        'required' attribute of the respective fields.  Example:

            # makes disciplines field required
            required_list = super(MyModel, cls).required_field_overrides()
            required_list.append('disciplines')
            return required_list
        """
        return ['organizations']

    @classmethod
    def required_metadata(cls):
        """
        Each content type has different requirements for metadata.
        For example:
         - a photo only requires an Image, but no Author or Files.
         - a conference presentation requires a file upload, but limits to 3
         - a publication requires either a document or a website

        To handle this we use a simple dictionary for each class. Here's an
        example of Photographs:
            {
                'website': {'max': 5, 'min': 0},  # optional, up to 5
                'image': {'max': 5, 'min': 1},  # one image is required
                # files are not included (no key)
                # authors are not included (no key)
            }
        And Course Materials:
            {
                # images not included
                'website': {'max': 5, 'min': 0},  # optional, up to 5
                'author': {'max': 5, 'min': 0},  # optional, up to 5
                'file': {'max': 3, 'min': 0},  # optional, up to 3
                # at least one file or website is required
                'conditionally_required': {'website', 'file'}
            }

        `conditionally_required` means that the at least one of the objects
        must be submitted with the resource.
        """
        return {}

    @classmethod
    def preset_topics(cls):
        """
        Some resource types require certain topics to be selected, like
        "Curriculum" for AcademicProgram

        return ['Curriculum']
        """
        return {}


@python_2_unicode_compatible
class Author(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="authors")
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=128, blank=True, null=True)
    organization = models.ForeignKey(
        'metadata.Organization', blank=True, null=True)
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
    label = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="The title of the document")
    item = models.FileField(
        help_text="Valid formats are aceptable: PDF, Excel, Word, PPT...")
    affirmation = models.BooleanField(
        'Affirmation of Ownership', default=False, help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Additional File'
        verbose_name_plural = 'Additional Files'

    def __str__(self):
        return self.label or 'File object'


@python_2_unicode_compatible
class Image(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="images")
    caption = models.CharField(max_length=500, blank=True, null=True)
    credit = models.CharField('Photographer credit', max_length=500, blank=True, null=True)
    image = models.ImageField(
        help_text="The following files formats are acceptable: JPEG, PNG,"
        " TIFF...")
    affirmation = models.BooleanField(
        'Affirmation of Ownership', default=False, help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Additional Image'
        verbose_name_plural = 'Additional Images'

    def __str__(self):
        return self.caption or 'Image object'

    def get_filename(self):
        return os.path.basename(self.image.name)

# =============================================================================
# Mapping of all available content types.
#
# We also load the content types here into the models namespace, so they are
# registered in the system, and the migration.
# =============================================================================
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

CONTENT_TYPES = OrderedDict()
CONTENT_TYPES['academicprogram'] = AcademicProgram
CONTENT_TYPES['casestudy'] = CaseStudy
CONTENT_TYPES['presentation'] = Presentation
CONTENT_TYPES['material'] = Material
CONTENT_TYPES['outreachmaterial'] = OutreachMaterial
CONTENT_TYPES['photograph'] = Photograph
CONTENT_TYPES['publication'] = Publication
CONTENT_TYPES['centerandinstitute'] = CenterAndInstitute
CONTENT_TYPES['tool'] = Tool
CONTENT_TYPES['video'] = Video
