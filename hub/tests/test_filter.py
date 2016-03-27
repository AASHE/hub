from django.utils.timezone import now
from django.core.urlresolvers import reverse

from ..apps.metadata.models import Organization, SustainabilityTopic
from ..apps.content.types.academic import AcademicProgram
from .base import BaseSearchBackendTestCase, WithUserSuperuserTestCase


class FilterTestCase(WithUserSuperuserTestCase, BaseSearchBackendTestCase):
    def setUp(self):
        """
        Create some sane default objects that will match almost all filter
        variants.
        """
        self.url_search = '{}?search=keyword'.format(reverse('browse:browse'))

        self.topic = SustainabilityTopic.objects.create(name='Curriculum')

        self.org = Organization.objects.create(
            account_num=1, org_name='Washington', country_iso='AUS',
            country='Australia', enrollment_fte=2000, exclude_from_website=0,
            carnegie_class="Associate", org_type="Business")

        self.ct = AcademicProgram.objects.create(
            title='My Keyword resource',
            status=AcademicProgram.STATUS_CHOICES.published,
            published=now())

        self.ct.topics.add(self.topic)
        self.ct.organizations.add(self.org)
        self.ct.keywords.add("tag 1")
        self.ct.keywords.add("tag2")

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
            # FIXME: If I provide a `country` filter argument, that filter is
            #        not even called. It is when I don't provide one.
            #        Why? Becaues required=False?
            # 'country': 'AUS',
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
