from json import loads

from django.test import TestCase
from django.core.urlresolvers import reverse

from ..apps.metadata.models import Organization
from ..apps.content.models import AcademicProgram


class BaseApiTestCase(TestCase):

    def _get_response(self, keyword):
        return self.client.get(self.api_url, data={'q': keyword})

    def min_length_test(self):
        """
        The api keyword needs to be at least 2 characters long.
        """
        response = self._get_response('')
        self.assertEqual(response.status_code, 400)

        response = self._get_response('a')
        self.assertEqual(response.status_code, 400)

        response = self._get_response('aa')
        self.assertEqual(response.status_code, 200)


class OrganizationsApiTestCase(BaseApiTestCase):
    """
    Test the organization matching API.
    """
    def setUp(self):
        self.api_url = reverse('api:organizations')
        defaults = {'exclude_from_website': '0'}
        self.org1 = Organization.objects.create(
            account_num=1, org_name='Washington',
            enrollment_fte=2000, **defaults)
        self.org2 = Organization.objects.create(
            account_num=2, org_name='New York',
            enrollment_fte=4000, **defaults)
        self.org3 = Organization.objects.create(
            account_num=3, org_name='Los York',
            enrollment_fte=12000, **defaults)

    def test_min_length(self):
        self.min_length_test()

    def test_json_and_matching(self):
        """
        The response is proper json and the matching is case insensitive.
        """
        response = self._get_response('york')
        self.assertEqual(response.status_code, 200)

        # If it's not JSON it fails here
        data = loads(response.content)

        # The response format is a list of dicionaries. 'york' will match our
        # org2 and org3 sample organization.
        self.assertTrue(isinstance(data, list))
        self.assertTrue(len(data), 2)

        # The response item contains the primary key and the organization name
        self.assertTrue('pk' in data[0])
        self.assertTrue('org_name' in data[0])

        # Dictionaries are not sorted
        # so we don't know the exact order, therefor compare the list against
        # a list.
        for match in data:
            self.assertTrue(match['pk'] in (self.org2.pk, self.org3.pk))


class KeywordsApiTestCase(BaseApiTestCase):
    """
    Test the keyword matching API.
    """
    def setUp(self):
        self.api_url = reverse('api:tags_autocomplete')
        self.ap = AcademicProgram.objects.create(
            title="Testing", status=AcademicProgram.STATUS_CHOICES.published)
        self.ap.keywords.add("pizza")
        
        AcademicProgram.keywords.tag_model.objects.create(name="bogustag")

    def test_min_length(self):
        self.min_length_test()

    def test_api_endpoint(self):
        """
        Confirm that the keyword is found
        """
        response = self._get_response('pi')
        self.assertEqual(response.status_code, 200)

        # If it's not JSON it fails here
        data = loads(response.content)

        # The respons includes pizza
        self.assertEqual(data[0]['name'], 'pizza')
        
        # Tags without resources shouldn't display
        self.assertEqual(AcademicProgram.keywords.tag_model.objects.count(), 2)
        response = self._get_response('bo')
        self.assertEqual(response.status_code, 200)
        data = loads(response.content)
        self.assertEqual(len(data), 0)
