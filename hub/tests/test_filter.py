import sys

from django.utils.timezone import now
from django.core.urlresolvers import reverse

from ..apps.metadata.models import (AcademicDiscipline,
                                    Organization,
                                    PublicationMaterialType,
                                    SustainabilityTopic)
from ..apps.content.types.academic import AcademicProgram
from ..apps.content.types.publications import Publication
from ..apps.content.models import CONTENT_TYPES
from .base import (EXTRA_REQUIRED_CT_KWARGS,
                   WithUserSuperuserTestCase)


class FilterTestCase(WithUserSuperuserTestCase):
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

        self.url_search = '{}?search=keyword'.format(reverse('browse:browse'))

        self.topic = SustainabilityTopic.objects.create(
            name='Curriculum', slug='curriculum')
        self.discipline = AcademicDiscipline.objects.create(name='Agriculture')

        self.org = Organization.objects.create(
            account_num=1, org_name='Washington', country_iso='AU',
            country='Australia', enrollment_fte=2000, exclude_from_website=0,
            carnegie_class="Associate", org_type="Business")

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

    def test_multi_filter_arguments(self):
        """
        Calls the 'browse' view with all possible filter arguments.

        - It does not test all of the filter logic itself
        - It does only match one resource, and only because we write the
          search pretty much exactly against it

        Though it forces each filter to execute it's `filter()` methods where
        the actual logic lays in. Simple programming errors would be caught
        easily here.
        """
        self.client.login(**self.superuser_cred)

        response = self.client.get(self.url_search, self.filter_data)

        # One item was found, our AcademicProgram
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)

        # The frontend does not list actual content types like "Academic
        # Program", it lists the Base classes, but there is an easy way to
        # fetch that one:
        self.assertTrue(
            self.ct.contenttype_ptr in response.context['object_list'])

    def test_org_type_filter(self):
        """
        Additional test for variable org_type filter
        """

        _filter_data = {'organization_type': ['Business']}
        _filter_data.update(self.filter_data)
        self.client.login(**self.superuser_cred)

        response = self.client.get(self.url_search, _filter_data)

        # One item was found, our AcademicProgram
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)

        _filter_data['organization_type'] = ['System']
        response = self.client.get(self.url_search, _filter_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 0)

    def test_search_handles_special_characters(self):
        """
        ElasticSearch has some characters that must be escaped
        Confirm that we escape them by appending them to the query
        to see if results are still returned.
        """
        self.client.login(**self.superuser_cred)
        url = "%s%s" % (self.url_search, '+-&|!\(\){}[]^"~*?:\\\/')

        response = self.client.get(url)

        # One item should still be returned
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 1)


class SpecificFilterTestCase(WithUserSuperuserTestCase):
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
