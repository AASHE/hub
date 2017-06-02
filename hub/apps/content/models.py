from __future__ import unicode_literals

from logging import getLogger
from collections import OrderedDict
from urlparse import urlparse

import tagulous

from django.conf import settings
from django.contrib.postgres.search import (SearchVector,
                                            SearchVectorField)
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from model_utils import Choices, FieldTracker
from model_utils.models import TimeStampedModel
from s3direct.fields import S3DirectField
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
    # The timestamp when this resource was marked PUBLISHED
    published = models.DateTimeField(
        blank=True,
        null=True,
        help_text='This timestamp is automatically set once the status becomes'
        ' "Published".',
        verbose_name='Date Posted')
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True)

    title = models.CharField(max_length=500)  # label set by self.title_label
    slug = models.CharField(max_length=500, blank=True)

    description = models.TextField(
        'Description', blank=True, null=True,
        help_text='''Styling with
        <a href="https://simplemde.com/markdown-guide" target="_blank">
        Markdown</a>
        is supported''')

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

    # This is the date the resource was created in the real world, not when
    # the instance was created in the db. That's stored in `created`.
    date_created = models.DateField(
        blank=True, null=True,
        verbose_name='Date Created, Published or Presented',
        help_text='''Enter the date when this resource was created, founded,
        published, or presented. If you don't know the exact date, choose the
        first day of the month. Use January 1 if you only know the year. You
        can use the calendar widget or type in a date in YYYY-MM-DD format.''')

    # This is the date the resourece was SUBMITTED TO THE HUB
    date_submitted = models.DateField(
        null=True, auto_now_add=True, verbose_name='Date Submitted')

    status_tracker = FieldTracker(fields=['status'])

    search_vector = SearchVectorField(blank=True, null=True)

    authors_search_data = models.TextField(blank=True, null=True, default='')
    files_search_data = models.TextField(blank=True, null=True, default='')
    images_search_data = models.TextField(blank=True, null=True, default='')

    objects = ContentTypeManager()

    class Meta:
        verbose_name = 'Generic Content Type'
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
            # For case studies, we want to copy the published date
            # into date_created as well
            if self.content_type == 'casestudy':
                self.date_created = self.published

        # Update the slug value on first save. This doesn't need to be unique
        # since the actual db URL lookup is still done with the pk.
        if not self.slug:
            self.slug = slugify(self.title)

        super(ContentType, self).save(*args, **kwargs)

        # TODO - only update self.search_vector when one the the
        # fields it includes changes.  Maybe.  Maybe unneccesary
        # optimization.
        ContentType.objects.filter(id=self.id).update(
            search_vector=SearchVector(
                'description',
                'title',
                'authors_search_data',
                'images_search_data',
                'files_search_data'))

    def get_absolute_url(self):
        return reverse('browse:view', kwargs={'ct': self.content_type,
                                              'id': self.pk,
                                              'slug': self.slug})

    def get_admin_url(self):
        return reverse('admin:content_{0}_change'.format(self.content_type),
                       args=[self.pk])

    def create_thumbnails(self, recreate=False):
        """
            Creates thumbnails for each image tied to this resource
        """
        from .tasks import thumbnail_image
        for image in self.images.all():
            thumbnail_image.delay(image.pk, recreate=recreate)

    def get_organization_list(self):
        return list(self.organizations.all())

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

    @classmethod
    def exclude_form_fields(cls):
        """
        Some resource types may exclude fields from the creation form, for
        example, CaseStudies exclude `date_created`
        """
        return []


@python_2_unicode_compatible
class Author(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="authors")
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=128, blank=True, null=True)
    organization = models.ForeignKey(
        'metadata.Organization', blank=True, null=True,
        on_delete=models.SET_NULL)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Website(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="websites")
    label = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField()

    def __str__(self):
        return self.label or 'Website object'

    def get_absolute_url(self):
        return self.ct.get_admin_url()


@python_2_unicode_compatible
class File(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="files")
    label = models.CharField(
        max_length=100, blank=True, null=True,
        help_text="The title of the document")
    item = S3DirectField(
        dest='files',
        help_text="Valid formats are aceptable: PDF, Excel, Word, PPT",
        blank=True, null=True)
    affirmation = models.BooleanField(
        'Affirmation of Ownership', default=False, help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Additional File'
        verbose_name_plural = 'Additional Files'

    def __str__(self):
        return self.label or 'File object'

    def get_filename(self):
        if self.item:
            p = urlparse(self.item)
            try:
                return p.path.split("/")[-1]
            except:
                pass
        return "No Name"


@python_2_unicode_compatible
class Image(TimeStampedModel):
    ct = models.ForeignKey(ContentType, related_name="images")
    caption = models.CharField(max_length=500, blank=True, null=True)
    credit = models.CharField(
        'Photographer credit', max_length=500, blank=True, null=True)
    image = S3DirectField(
        dest='images', help_text="JPG and PNG file formats are accepted",
        blank=True, null=True)
    small_thumbnail = models.URLField(
        default="/static/img/100x100_blank.png")
    med_thumbnail = models.URLField(
        default="/static/img/300x300_blank.png")
    affirmation = models.BooleanField(
        'Affirmation of Ownership', default=False, help_text=AFFIRMATION)

    class Meta:
        verbose_name = 'Additional Image'
        verbose_name_plural = 'Additional Images'

    def __str__(self):
        return self.caption or 'Image object'

    def get_absolute_url(self):
        return self.ct.get_admin_url()


# =============================================================================
# Mapping of all available content types.
#
# We also load the content types here into the models namespace, so they are
# registered in the system, and the migration.
# =============================================================================
from .types.academic import AcademicProgram  # noqa
from .types.casestudies import CaseStudy  # noqa
from .types.centers import CenterAndInstitute  # noqa
from .types.courses import Material  # noqa
from .types.outreach import OutreachMaterial  # noqa
from .types.photographs import Photograph  # noqa
from .types.presentations import Presentation  # noqa
from .types.publications import Publication  # noqa
from .types.tools import Tool  # noqa
from .types.videos import Video  # noqa

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
