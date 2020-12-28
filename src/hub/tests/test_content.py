from django.contrib.auth.models import User
from django.core import mail
from django_webtest import WebTest

from ..apps.content.types.videos import Video
from ..apps.content.types.casestudies import CaseStudy
from ..apps.content.models import Website
from ..apps.metadata.models import (Organization,
                                    SustainabilityTopic,
                                    InstitutionalOffice)


class AdminTestCase(WebTest):

    def setUp(self):
        super(AdminTestCase, self).setUp()
        self.superuser = User.objects.create_superuser(
            first_name='Super',
            last_name='User',
            email='superuser@example.com',
            username='superuser',
            password='password'
        )

        self.resource = Video.objects.create(content_type='video',
                                             status='new',
                                             permission='open',
                                             title='Test Video Resource',
                                             slug='test-video-resource',
                                             submitted_by=self.superuser)

        self.resource.websites.add(
            Website.objects.create(
                ct=self.resource,
                url="http://www.aashe.org/video.mp4"))
        self.resource.organizations.add(
            Organization.objects.create(account_num=1,
                                        org_name='Hipster University',
                                        exclude_from_website=0))
        self.resource.topics.add(
            SustainabilityTopic.objects.create(name='Science', slug='science'))
        self.resource.institutions.add(
            InstitutionalOffice.objects.create(name='Lirum'))
        self.resource.save()

    def _post_resource(self, status):
        response = self.app.get(self.resource.get_admin_url(),
                                user=self.superuser.username)
        response.form['status'] = status
        return response.form.submit()

    def test_mail_is_sent_upon_resource_approval(self):
        self._post_resource('published')
        self.assertEqual(1, len(mail.outbox))
        self.assertIn('approved', mail.outbox[0].subject.lower())

    def test_mail_is_sent_upon_resource_rejection(self):
        self._post_resource('declined')
        self.assertEqual(1, len(mail.outbox))
        self.assertIn('declined', mail.outbox[0].subject.lower())

    def test_case_study_date_fields(self):
        case_study = CaseStudy.objects.create(content_type='casestudy',
                                              status='new',
                                              permission='open',
                                              title='Test Case Study',
                                              slug='test-case-study',
                                              submitted_by=self.superuser,
                                              consider_for_award=False)

        self.assertEqual(case_study.date_created, None)
        case_study.status = case_study.STATUS_CHOICES.published
        case_study.save()
        self.assertEqual(case_study.published, case_study.date_created)
