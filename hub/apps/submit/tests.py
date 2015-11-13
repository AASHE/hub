from django.core.urlresolvers import reverse

from ..metadata.models import AcademicDiscipline, Organization, \
    SustainabilityTopic
from ..content.types.videos import Video
from ..browse.tests import WithUserSuperuserTestCase

class SubmitVideoTestCase(WithUserSuperuserTestCase):
    """
    Tests around a content type submission. In this case a Video, since it
    has the least complex fieldset.
    """
    def setUp(self):
        self._organization = Organization.objects.create(account_num=1,
            org_name='Hipster University', exclude_from_website=0)
        self._discipline = AcademicDiscipline.objects.create(name='Jumping')
        self._topic = SustainabilityTopic.objects.create(name='Science')

        self.form_url = reverse('submit:form', kwargs={'ct': 'video'})
        self.form_valid_data = {
            # Document Form
            'document-title': 'My first Video',
            'document-link': 'http://example.com/video.mp4',
            'document-affirmation': True,
            'document-organizations': [self._organization.pk],
            'document-disciplines': [self._discipline.pk],
            'document-topics': [self._topic.pk],

            # Formset management forms
            #
            # OPTIMIZE: can we automate this, get all this context data from
            #           `SubmitView.get_forms()`?
            'authors-TOTAL_FORMS': 5,
            'authors-INITIAL_FORMS': 0,
            'authors-MIN_NUM_FORMS': 0,
            'authors-MAX_NUM_FORMS': 5,

            'images-TOTAL_FORMS': 5,
            'images-INITIAL_FORMS': 0,
            'images-MIN_NUM_FORMS': 0,
            'images-MAX_NUM_FORMS': 5,

            'files-TOTAL_FORMS': 5,
            'files-INITIAL_FORMS': 0,
            'files-MIN_NUM_FORMS': 0,
            'files-MAX_NUM_FORMS': 5,

            'websites-TOTAL_FORMS': 5,
            'websites-INITIAL_FORMS': 0,
            'websites-MIN_NUM_FORMS': 0,
            'websites-MAX_NUM_FORMS': 5,
        }
        return super(SubmitVideoTestCase, self).setUp()

    def _post_video(self, form_data=None):
        data = self.form_valid_data
        if form_data:
            data.update(form_data)
        return self.client.post(self.form_url, data, follow=True)

    def test_invalid_content_type_gives_404(self):
        self.client.logout()
        form_url = form_url = reverse('submit:form', kwargs={'ct': 'doesnotexist'})
        response = self.client.get(form_url)
        self.assertEqual(response.status_code, 404)

    def test_user_needs_logged_in_to_see_form(self):
        self.client.logout()
        response = self.client.get(self.form_url)
        self.assertEqual(response.status_code, 403)

    def test_user_needs_logged_in_to_submit(self):
        self.client.logout()
        response = self._post_video()
        self.assertEqual(response.status_code, 403)

    def test_logged_in_user_can_see_form(self):
        self.client.login(**self.user_cred)
        response = self.client.get(self.form_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('document_form' in response.context)

    def test_valid_video_with_no_formsets(self):
        """
        Create a new video and check that all its auto-related data is sane.
        Videos are very simple, they only need a video_link and title set, and
        we don't add much more than that here.
        """
        self.client.login(**self.user_cred)
        response = self._post_video()

        #print response.context['document_form']._errors

        # Video was created
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Video.objects.count(), 1)

        # The user is associated with the new content type and it's marked
        # as new. By default new content types are 'member only'.
        video = Video.objects.all()[0]
        self.assertEqual(video.submitted_by, self.user)
        self.assertEqual(video.status, Video.STATUS_CHOICES.new)
        self.assertEqual(video.permission, Video.PERMISSION_CHOICES.member)

        self.assertEqual(video.title, self.form_valid_data['document-title'])
        self.assertEqual(video.link, self.form_valid_data['document-link'])

        # We didn't added any formsets yet, so they must be empty
        self.assertEqual(video.authors.count(), 0)
        self.assertEqual(video.images.count(), 0)
        self.assertEqual(video.files.count(), 0)
        self.assertEqual(video.websites.count(), 0)

    def test_valid_video_with_authors(self):
        """
        Test that additional formset authors are saved along. This would apply
        to files, images and websites as well.
        """
        additional_data = {
            'authors-0-name': 'Martin',
            'authors-0-email': 'martin@example.com',
            'authors-0-title': 'Head of Regular Expressions',

            'authors-1-name': 'Donald Duck',
            'authors-1-email': 'dd@example.com',
            'authors-1-title': 'Head of Entenhausen',
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
        self.assertEqual(video.websites.count(), 0)

        names = video.authors.values_list('name', flat=True)
        self.assertTrue('Martin' in names)
        self.assertTrue('Donald Duck' in names)


    def test_user_is_author_feature(self):
        """
        If a user submits 'I am an author' we save the logged in user object
        as an author.
        """
        additional_data = {
            'document-user_is_author': True
        }

        self.client.login(**self.user_cred)
        response = self._post_video(additional_data)

        # Video was created
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Video.objects.count(), 1)

        # The author was automatically created, it's name and email
        # were taken from the logged in user account
        video = Video.objects.all()[0]
        self.assertEqual(video.authors.count(), 1)
        self.assertEqual(video.authors.all()[0].name, self.user.get_full_name())
        self.assertEqual(video.authors.all()[0].email, self.user.email)

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
