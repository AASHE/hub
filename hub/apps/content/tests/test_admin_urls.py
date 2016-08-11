from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.test.client import RequestFactory

from datetime import datetime

from hub.apps.content.models import (
    AcademicProgram,
    CaseStudy,
    CenterAndInstitute,
    Material,
    OutreachMaterial,
    Photograph,
    Presentation,
    Publication,
    Tool,
    Video,
    CONTENT_TYPES)
from ...metadata.models import (
    Organization,
    SustainabilityTopic,
    InstitutionalOffice)
from hub.apps.content.admin import (
    BaseContentTypeAdmin,
    SpecificContentTypeAdmin,
    AllContentTypesAdmin)
from hub.apps.content.models import ContentType


class AdminURLTestCase(TestCase):
    """
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
    """

    def setUp(self):
        self.user = User.objects.create_superuser(
            first_name='Super',
            last_name='User',
            email='superuser@example.com',
            username='superuser',
            password='password'
        )
        self.org = Organization.objects.create(
            account_num=1, org_name='Hipster U', exclude_from_website=0)
        self.topic = SustainabilityTopic.objects.create(
            name='Science', slug='science')
        self.office = InstitutionalOffice.objects.create(name='Lirum')

        self.generic_properties = {
            'status': 'new',
            'permission': 'open',
            'published': datetime.now(),
            'submitted_by': self.user,
            'title': "test resource",
            'slug': "test_resource",
            'description': "testing this",
            'date_created': datetime.now()
        }

        self.ct_specific_fields = {
            'casestudy': {
                'consider_for_award': False
            }
        }
        self.client = Client()

    def test_admin_urls(self):
        """
        Create each content type and then get the admin_url
        """
        for key, klass in CONTENT_TYPES.items():
            prop_dict = self.generic_properties.copy()
            prop_dict.update({
                'content_type': key,
            })
            if key in self.ct_specific_fields.keys():
                prop_dict.update(self.ct_specific_fields[key])
            ct = klass.objects.create(**prop_dict)
            # just make sure no exceptions are raised
            url = ct.get_admin_url()

    def test_admin_content_functions(self):
        """
        Verify that the admin actions successfully
        publish, unpublish, and decline content.
        """
        # Need a user object to avoid errors when utils.send_resource_* methods
        # are called upon success
        user = User.objects.create_user('test_user', email='test@aashe.org')
        # Set that user as submitted_by for our test content piece
        content = Video.objects.create(submitted_by=user)
        # Verify this was all set up with the correct attribute values
        self.assertEqual(content.status, 'new')
        self.assertEqual(content.submitted_by.email, 'test@aashe.org')

        # Create the request object needed as argument for admin methods
        request = RequestFactory().get('/admin/content/contenttype/')
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # Instantiate admin site so we can call its methods directly
        content_admin = AllContentTypesAdmin(ContentType, AdminSite())

        # Test Publish Action (need to retrieve queryset to operate on first)
        queryset = Video.objects.filter(pk=1)
        self.assertEqual(queryset[0].status, 'new')
        self.assertTrue(queryset)
        content_admin.publish(request, queryset)
        queryset = Video.objects.filter(pk=1)
        self.assertTrue(queryset)
        self.assertEqual(queryset[0].status, 'published')
        self.assertEqual(1, len(mail.outbox))
        self.assertTrue("Content type: Videos" in mail.outbox[0].body)

        # Test Unpublish Action
        # (status is already 'published' and queryset loaded)
        content_admin.unpublish(request, queryset)
        queryset = Video.objects.filter(pk=1)
        self.assertTrue(queryset)
        self.assertEqual(queryset[0].status, 'new')

        # Test Decline Action (status already 'new' and queryset loaded)
        content_admin.decline(request, queryset)
        queryset = Video.objects.filter(pk=1)
        self.assertTrue(queryset)
        self.assertEqual(queryset[0].status, 'declined')
        self.assertEqual(2, len(mail.outbox))
        self.assertTrue("Content type: Videos" in mail.outbox[1].body)

        # confirm that no emails are sent when changing status from anything
        # other than 'new'

        # declined > published
        queryset = Video.objects.filter(pk=1)
        self.assertEqual(queryset[0].status, 'declined')
        content_admin.publish(request, queryset)

        queryset = Video.objects.filter(pk=1)
        self.assertEqual(queryset[0].status, 'published')
        self.assertEqual(2, len(mail.outbox))  # no additional emails

        # published > declined
        queryset = Video.objects.filter(pk=1)
        self.assertEqual(queryset[0].status, 'published')
        content_admin.decline(request, queryset)

        queryset = Video.objects.filter(pk=1)
        self.assertEqual(queryset[0].status, 'declined')
        self.assertEqual(2, len(mail.outbox))  # no additional emails
