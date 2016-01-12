from django.contrib.auth.models import User
from django.test import TestCase

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
        self.topic = SustainabilityTopic.objects.create(name='Science')
        self.office = InstitutionalOffice.objects.create(name='Lirum')

        self.generic_properties = {
            'status': 'new',
            'permission': 'open',
            'published': datetime.now(),
            'submitted_by': self.user,
            'title': "test resource",
            'slug': "test_resource",
            'description': "testing this",
        }

        self.ct_specific_fields = {
            'presentation': {
                'date': datetime.now()
            }
        }

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
