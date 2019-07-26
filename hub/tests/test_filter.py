from django.utils.timezone import now
from django.conf import settings
from django.urls import reverse

from ..apps.metadata.models import Organization, SustainabilityTopic, \
    AcademicDiscipline, PublicationMaterialType, FundingSource
from ..apps.content.types.academic import AcademicProgram
from ..apps.content.types.photographs import Photograph
from ..apps.content.types.publications import Publication
from ..apps.content.types.green_funds import GreenFund
from ..apps.content.models import CONTENT_TYPES, Image
from .base import (
    BaseSearchBackendTestCase,
    WithUserSuperuserTestCase,
    EXTRA_REQUIRED_CT_KWARGS)

import sys


class FilterTestCase(WithUserSuperuserTestCase, BaseSearchBackendTestCase):
    def setUp(self):
        """
        Create some sane default objects that will match almost all filter
        variants.
        """

        # clear/reload the filter modules because their __init__ methods
        # need to be called again
        modules = ["hub.apps.browse.filter", "hub.apps.browse.filterset"]
        for module in modules:
            if module in sys.modules.keys():
                del sys.modules[module]

        self.url_search = '{}?search='.format(reverse('browse:browse'))

        self.topic = SustainabilityTopic.objects.create(
            name='Curriculum', slug='curriculum')
        self.discipline = AcademicDiscipline.objects.create(name='Agriculture')

        self.org = Organization.objects.create(
            account_num=1, org_name='Washington', country_iso='AU',
            country='Australia', enrollment_fte=2000, exclude_from_website=0,
            carnegie_class="Associate")  # , org_type="Business")

        self.ct = AcademicProgram.objects.create(
            title='My Keyword resource',
            date_created=now(),
            status=AcademicProgram.STATUS_CHOICES.published,
            published=now())

        self.ct.topics.add(self.topic)
        self.ct.organizations.add(self.org)
        self.ct.keywords.add("tag 1")
        self.ct.keywords.add("tag2")
        self.ct.disciplines.add(self.discipline)

        # Update search index
        self._rebuild_index()

        self.filter_data = {
            'search': 'keyword',
            'topics': [self.topic.slug],
            'content_type': ['academicprogram'],
            'organizations': [self.org.pk],
            'tag_filter': ['tag 1'],
            'organization_type': ['Associate'],
            'size': ['lt_5000'],
            'published': self.ct.published.year,
            'date_created': now().year,
            'disciplines': [self.discipline],
            'country': 'AU',
            'order': 'title',
        }

        return super(FilterTestCase, self).setUp()

    # get this working
    # def test_search_handles_special_characters(self):


class SpecificFilterTestCase(WithUserSuperuserTestCase, BaseSearchBackendTestCase):
    """
    Test some specific filters for different content types
    """

    def test_pub_type_filter(self):
        """
        Test for the publication type filter
        """
        type_1 = PublicationMaterialType.objects.create(name="Type 1")
        type_2 = PublicationMaterialType.objects.create(name="Type 2")

        ct = Publication.objects.create(
            title='Test Publication 1',
            material_type=type_1,
            published=now(),
            status=Publication.STATUS_CHOICES.published,
        )

        ct2 = Publication.objects.create(
            title='Test Publication 2',
            material_type=type_2,
            published=now(),
            status=Publication.STATUS_CHOICES.published,
        )

        _url = reverse('browse:browse', kwargs={'ct': 'publication'})
        _filter_data = {'publication_type': [type_1.pk]}
        self.client.login(**self.superuser_cred)

        response = self.client.get(_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

        response = self.client.get(_url, _filter_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)

    def test_date_created_filter(self):
        """
        Each content type has a slightly different implementation of the
        date_created filter (prepopulated with relevant dates)
        """

        for k, ct_class in CONTENT_TYPES.items():

            if k == 'greenfund':
                st = SustainabilityTopic.objects.create(
                    name='Blah', slug='blah')
                fs = FundingSource.objects.create(name='Junk')
                gf = GreenFund.objects.create(
                    title='blah',
                    description='blah',
                    date_created=now(),
                    published=now(),
                    status=ct_class.STATUS_CHOICES.published,
                    revolving_fund='Yes',
                )
                gf.topics.add(st)
                gf.funding_sources.add(fs)
            else:
                ct_kwargs = {
                    'title': 'Date Created Resource',
                    'date_created': now(),
                    'status': ct_class.STATUS_CHOICES.published,
                    'published': now(),
                }
                if k in EXTRA_REQUIRED_CT_KWARGS.keys():
                    ct_kwargs.update(EXTRA_REQUIRED_CT_KWARGS[k])

                ct = ct_class.objects.create(**ct_kwargs)

            _url = reverse('browse:browse', kwargs={'ct': k})
            _filter_data = {'date_created': [now().year]}
            self.client.login(**self.superuser_cred)

            response = self.client.get(_url, _filter_data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['object_list']), 1)


class TestGalleryView(WithUserSuperuserTestCase, BaseSearchBackendTestCase):
    """
        Test the gallery view

        - ensure filter is working properly (only resources with images)
    """

    def setUp(self):

        super(TestGalleryView, self).setUp()

        self.resource1 = Photograph.objects.create(
            status=Photograph.STATUS_CHOICES.published,
            title='Test Photo Resource',
            slug='test-photo-resource',
            submitted_by=self.superuser
        )
        self.resource2 = Photograph.objects.create(
            status=Photograph.STATUS_CHOICES.published,
            title='Test Photo Resource',
            slug='test-photo-resource',
            submitted_by=self.superuser
        )
        img1 = Image.objects.create(
            ct=self.resource1,
            image="http://testserver%stest/sold.jpg" % settings.STATIC_URL,
            affirmation=True,
            caption="test caption one",
            credit="test credit one"
        )
        img2 = Image.objects.create(
            ct=self.resource1,
            image="http://testserver%stest/sold.jpg" % settings.STATIC_URL,
            affirmation=True,
            caption="test caption two",
            credit="test credit two"
        )

    def test_view(self):

        _url = reverse(
            'browse:browse',
            kwargs={'ct': 'photograph'})

        # test the list view - should show both resources
        _filter_data = {'gallery_view': 'list'}
        response = self.client.get(_url, _filter_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 2)

        # test the gallery view
        # @todo - should the object list be image objects... and therefore 2?
        # decision needed
        _filter_data = {'gallery_view': 'gallery'}
        response = self.client.get(_url, _filter_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)
