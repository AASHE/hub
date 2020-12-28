from unittest import TestCase

from ..apps.metadata.models import Organization


class OrganizationProxyTestCase(TestCase):
    def setUp(self):
        defaults = {'exclude_from_website': '0'}
        self.org1 = Organization.objects.create(
            account_num=1, org_name='Washington',
            enrollment_fte=2000, **defaults)
        self.org2 = Organization.objects.create(
            account_num=2, org_name='New York',
            enrollment_fte=4000, **defaults)
        self.org3 = Organization.objects.create(
            account_num=3, org_name='Los Angeles',
            enrollment_fte=12000, **defaults)

    def tearDown(self):
        Organization.objects.all().delete()

    def test_fte_range_max_only(self):
        org_list = Organization.objects.in_fte_range(max=5000)
        self.assertIn(self.org1, org_list)
        self.assertIn(self.org2, org_list)
        self.assertNotIn(self.org3, org_list)

    def test_fte_range_min_only(self):
        org_list = Organization.objects.in_fte_range(min=5000)
        self.assertNotIn(self.org1, org_list)
        self.assertNotIn(self.org2, org_list)
        self.assertIn(self.org3, org_list)

    def test_fte_range_min_max(self):
        org_list = Organization.objects.in_fte_range(min=4000, max=12000)
        self.assertNotIn(self.org1, org_list)
        self.assertIn(self.org2, org_list)
        self.assertIn(self.org3, org_list)
