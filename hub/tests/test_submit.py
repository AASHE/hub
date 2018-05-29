from django.core import mail
import os

from django.core.urlresolvers import reverse
from django.conf import settings
from django.test import override_settings

from ..apps.metadata.models import AcademicDiscipline, Organization, \
    SustainabilityTopic, InstitutionalOffice, CourseMaterialType
from ..apps.content.types.videos import Video
from ..apps.content.types.courses import Material
from ..apps.content.types.casestudies import CaseStudy
from .base import WithUserSuperuserTestCase


@override_settings(CELERY_ALWAYS_EAGER=True)
class SubmitResourceTestCase(WithUserSuperuserTestCase):
    """
    Tests around a content type submission. In this case a Video, since it
    has the least complex fieldset.
    """
    def setUp(self):
        self.video_form_url = reverse('submit:form', kwargs={'ct': 'video'})
        self.material_form_url = reverse(
            'submit:form', kwargs={'ct': 'material'})
        self.casestudy_form_url = reverse(
            'submit:form', kwargs={'ct': 'casestudy'})

        self.video_form_valid_data = {
            # Document Form
            'document-title': 'My first Video',
            'document-description': 'blah',
            'document-affirmation': True,
            'document-keywords': "tag 1, tag 2",

            'document-organizations': [
                Organization.objects.create(account_num=1,
                                            org_name='Hipster University',
                                            exclude_from_website=0).pk
            ],
            'document-disciplines': [
                AcademicDiscipline.objects.create(name='Jumping').pk
            ],
            'document-topics': [
                SustainabilityTopic.objects.create(
                    name='Science', slug='science').pk,
                SustainabilityTopic.objects.create(
                    name="Curriculum", slug='curriculum').pk
            ],
            'document-institutions': [
                InstitutionalOffice.objects.create(name='Lirum').pk
            ],

            # Formset management forms
            #
            # OPTIMIZE: can we automate this, get all this context data from
            #           `SubmitView.get_forms()`?
            'author-TOTAL_FORMS': 0,
            'author-INITIAL_FORMS': 0,
            'author-MIN_NUM_FORMS': 0,
            'author-MAX_NUM_FORMS': 5,

            'website-TOTAL_FORMS': 0,
            'website-INITIAL_FORMS': 0,
            'website-MIN_NUM_FORMS': 0,
            'website-MAX_NUM_FORMS': 5,

            'file-TOTAL_FORMS': 0,
            'file-INITIAL_FORMS': 0,
            'file-MIN_NUM_FORMS': 0,
            'file-MAX_NUM_FORMS': 5,
        }

        self.material_form_valid_data = {}
        self.material_form_valid_data.update(self.video_form_valid_data)
        material, created = CourseMaterialType.objects.get_or_create(
            name="assignment")
        self.material_form_valid_data.update({
            'document-material_type': material.pk,
            'file-TOTAL_FORMS': 0,
            'file-INITIAL_FORMS': 0,
            'file-MIN_NUM_FORMS': 0,
            'file-MAX_NUM_FORMS': 5
        })

        self.casestudy_form_valid_data = {}
        self.casestudy_form_valid_data.update(self.video_form_valid_data)
        self.casestudy_form_valid_data.update({
            'document-financing': 'blah',
            'document-lessons_learned': 'blah',
            'document-description': 'blah',
            'document-implementation': 'blah',
            'document-timeline': 'blah',
            'document-results': 'blah',
            'document-goals': 'blah',
            'document-background': 'blah'
        })

        self.video_form_valid_data.update({
            'website-TOTAL_FORMS': 1,
            'website-MIN_NUM_FORMS': 1,
            'website-0-url': 'http://example.com/video.mp4',
        })

        SustainabilityTopic.objects.create(name="Research", slug='research')

        return super(SubmitResourceTestCase, self).setUp()

    def _post_video(self, form_data=None):
        data = self.video_form_valid_data
        if form_data:
            data.update(form_data)
        return self.client.post(self.video_form_url, data, follow=True)

    def _post_material(self, form_data=None):
        data = self.material_form_valid_data
        if form_data:
            data.update(form_data)
        return self.client.post(self.material_form_url, data, follow=True)

    def _post_casestudy(self, form_data=None):
        data = self.casestudy_form_valid_data
        if form_data:
            data.update(form_data)
        return self.client.post(self.casestudy_form_url, data, follow=True)

    def test_invalid_content_type_gives_404(self):
        self.client.logout()
        form_url = form_url = reverse('submit:form',
                                      kwargs={'ct': 'doesnotexist'})
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 404)

    def test_user_needs_logged_in_to_see_form(self):
        self.client.logout()
        response = self.client.get(self.video_form_url)
        self.assertEqual(response.status_code, 403)

    def test_user_needs_logged_in_to_submit(self):
        self.client.logout()
        response = self._post_video()
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_can_see_form(self):
        self.client.login(**self.user_cred)
        response = self.client.get(self.video_form_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('document_form' in response.context)

    def test_valid_video_with_link_formset(self):
        """
        Create a new video and check that all its auto-related data is sane.
        Videos are very simple, they only need a link and title set, and
        we don't add much more than that here.
        """
        self.client.login(**self.user_cred)
        response = self._post_video()

        # print response.context['document_form']._errors

        # Video was created
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Video.objects.count(), 1)

        # The user is associated with the new content type and it's marked
        # as new. By default new content types are 'member only'.
        video = Video.objects.all()[0]
        self.assertEqual(video.submitted_by, self.user)
        self.assertEqual(video.status, Video.STATUS_CHOICES.new)
        self.assertEqual(video.permission, Video.PERMISSION_CHOICES.member)

        self.assertEqual(
            video.title, self.video_form_valid_data['document-title'])
        self.assertEqual(video.websites.count(), 1)

        # We didn't added any formsets yet, so they must be empty
        self.assertEqual(video.authors.count(), 0)
        self.assertEqual(video.images.count(), 0)
        self.assertEqual(video.files.count(), 0)
        self.assertEqual(video.websites.count(), 1)
        self.assertEqual(video.keywords.count(), 2)

    def test_valid_video_with_authors(self):
        """
        Test that additional formset authors are saved along. This would apply
        to files, images and websites as well.
        """
        additional_data = {
            'author-0-name': 'Martin',
            'author-0-email': 'martin@example.com',
            'author-0-title': 'Head of Regular Expressions',

            'author-1-name': 'Donald Duck',
            'author-1-email': 'dd@example.com',
            'author-1-title': 'Head of Entenhausen',

            'author-TOTAL_FORMS': '2'
        }

        self.client.login(**self.user_cred)
        response = self._post_video(additional_data)

        # Video was created
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Video.objects.count(), 1)

        # as new. By default new content types are 'member only'.
        video = Video.objects.all()[0]
        self.assertEqual(video.authors.count(), 2)
        self.assertEqual(video.images.count(), 0)
        self.assertEqual(video.files.count(), 0)
        self.assertEqual(video.websites.count(), 1)

        names = video.authors.values_list('name', flat=True)
        self.assertIn('Martin', names)
        self.assertIn('Donald Duck', names)

        # test the __str__ method
        self.assertIn(str(video.authors.all()[0]), ['Martin', 'Donald Duck'])

    def test_user_is_author_feature(self):
        """
        Confirm that the user's information is populated in the optional author
        form
        """
        self.client.login(**self.user_cred)
        response = self.client.get(self.video_form_url, follow=True)
        self.assertEqual(
            response.context['user_is_author_form']['email'].field.initial,
            self.user.email)

    def test_invalid_form_shows_up_again(self):
        """
        A form with invalid, or missing required data is just showed up again
        and doesn't error out.
        """
        # Set the required title field to an empty string.
        additional_data = {
            'document-title': '',
        }

        self.client.login(**self.user_cred)
        response = self._post_video(additional_data)

        # The response code is 200, the new form is OK, however no video was
        # created and we have an error in our document form.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Video.objects.count(), 0)
        self.assertEqual(len(response.context['document_form']._errors), 1)

    def test_at_most_three_disciplines_topics_institutes(self):
        """
        The frontend forms allow at most 3 of each.
        """
        # Set the required title field to an empty string.
        additional_data = {
            'document-disciplines': [
                AcademicDiscipline.objects.create(name='Item 1').pk,
                AcademicDiscipline.objects.create(name='Item 2').pk,
                AcademicDiscipline.objects.create(name='Item 3').pk,
                AcademicDiscipline.objects.create(name='Item 4').pk,
            ],
            'document-topics': [
                SustainabilityTopic.objects.create(name='Item 1', slug='1').pk,
                SustainabilityTopic.objects.create(name='Item 2', slug='2').pk,
                SustainabilityTopic.objects.create(name='Item 3', slug='3').pk,
                SustainabilityTopic.objects.create(name='Item 4', slug='4').pk,
            ],
            'document-institutions': [
                InstitutionalOffice.objects.create(name='Item 1').pk,
                InstitutionalOffice.objects.create(name='Item 2').pk,
                InstitutionalOffice.objects.create(name='Item 3').pk,
                InstitutionalOffice.objects.create(name='Item 4').pk,
            ],
        }
        self.client.login(**self.user_cred)
        response = self._post_video(additional_data)

        # print response.context['document_form']._errors

        # The response code is 200, the new form is OK, however no video was
        # created and we have an errors in our document form.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Video.objects.count(), 0)
        self.assertEqual(len(response.context['document_form']._errors), 3)

    def test_valid_material_with_files(self):
        """

        """
        additional_data = {
            'file-0-label': 'test file',
            'file-0-item':
                "http://testserver%stest/test.csv" % settings.STATIC_URL,
            'file-0-affirmation': 'on',
            'file-TOTAL_FORMS': '1',
        }
        # filepath = os.path.join(os.path.dirname(__file__), 'media/test.txt')

        self.client.login(**self.user_cred)
        response = self._post_material(additional_data)

        # Material was created
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Material.objects.count(), 1)

        # as new. By default new content types are 'member only'.
        material = Material.objects.all()[0]
        self.assertEqual(material.files.count(), 1)

        f = material.files.all()[0]
        self.assertEqual('test file', f.label)
        self.assertRegexpMatches(f.item, '.*test.csv')
        self.assertEqual(f.get_filename(), 'test.csv')

    def test_required_metadata(self):
        """
        Test that the required_metadata method and resulting form validation

        materials require {'websites', 'files'}
        """
        self.client.login(**self.user_cred)
        response = self._post_material()
        err = response.context['document_form']._errors['__all__']
        self.assertEqual(
            err[0],
            "At least one website or file is required for this resource.")

        additional_data = {
            'website-0-label': 'aashe',
            'website-0-url': 'http://www.aashe.org',
            'website-TOTAL_FORMS': '1',
        }
        response = self._post_material(additional_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Material.objects.count(), 1)
        self.assertEqual(Material.objects.all()[0].websites.count(), 1)

    def test_email_is_sent_upon_submission(self):
        """Is an email sent when a resource is submitted?
        """
        self.client.login(**self.user_cred)
        self._post_video()
        self.assertEqual(1, len(mail.outbox))
        self.assertIn('review', mail.outbox[0].subject.lower())

    def test_required_topics(self):
        """
        Some content types require specific topics
        """

        additional_data = {
            'document-topics': [
                SustainabilityTopic.objects.get(name='Science').pk,
            ],
            'file-0-label': 'test file',
            'file-0-item':
                "http://testserver%stest/test.csv" % settings.STATIC_URL,
            'file-0-affirmation': 'on',
            'file-TOTAL_FORMS': '1',
        }

        self.client.login(**self.user_cred)

        response = self._post_material(additional_data)
        self.assertEqual(
            response.context['document_form']._errors['topics'],
            [u'The following topics are required: Curriculum'])

        additional_data.update({
            'document-topics': [
                SustainabilityTopic.objects.get(name="Curriculum").pk,
            ]
        })
        # with open(filepath) as upload:
        #     additional_data['file-0-item'] = upload
        response = self._post_material(additional_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Material.objects.count(), 1)

    def test_exclude_form_fields(self):
        """
        Some content types exclude fields from their forms
        """
        self.client.login(**self.user_cred)
        html = '''
        <input
            id="id_document-date_created"
            name="document-date_created"
            type="text">
        '''

        # case studies exclude date_created
        response = self.client.get(self.casestudy_form_url)
        self.assertNotContains(response, html, html=True)

        # materials include date_created
        response = self.client.get(self.material_form_url)
        self.assertContains(response, html, html=True)

    def test_image_thumbnailing(self):
        """
        Test that images get thumbnailed properly right after submission
        """
        additional_data = {
            'document-topics': [
                SustainabilityTopic.objects.get(name='Science').pk,
            ],
            'image-0-label': 'test file',
            'image-0-image':
                "http://testserver%stest/sold.jpg" % settings.STATIC_URL,
            'image-0-affirmation': 'on',
            'image-TOTAL_FORMS': '1',
            'image-INITIAL_FORMS': 0,
            'image-MIN_NUM_FORMS': 1,
            'image-MAX_NUM_FORMS': 5,

            'author-0-name': 'Martin',
            'author-0-email': 'martin@example.com',
            'author-0-title': 'Head of Regular Expressions',

            'author-TOTAL_FORMS': '1'
        }

        self.client.login(**self.user_cred)
        response = self._post_casestudy(additional_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(CaseStudy.objects.count(), 1)
        img = CaseStudy.objects.all()[0].images.all()[0]
        self.assertNotEqual(img.med_thumbnail, '/static/img/300x300_blank.png')
        self.assertTrue('cache' in img.med_thumbnail)
        self.assertNotEqual(
            img.small_thumbnail, '/static/img/100x100_blank.png')
        self.assertTrue('cache' in img.small_thumbnail)
