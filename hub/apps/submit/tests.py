from django.core.urlresolvers import reverse

from ..content.types.videos import Video
from ..browse.tests import WithUserSuperuserTestCase

class SubmitVideoTestCase(WithUserSuperuserTestCase):
    """
    Tests around a content type submission. In this case a Video, since it
    has the least complex fieldset.
    """
    def setUp(self):
        self.form_url = reverse('submit:form', kwargs={'ct': 'video'})
        self.form_valid_data = {
            # Document Form
            'document-title': 'My first Video',
            'document-video_link': 'http://example.com/video.mp4',
            'document-affirmation': True,

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

    def _post_video(self, **form_data):
        data = self.form_valid_data
        data.update(form_data)

        return self.client.post(self.form_url, data, follow=True)

    def test_user_needs_logged_in_to_submit(self):
        self.client.logout()
        response = self._post_video()
        self.assertEqual(response.status_code, 403)

    def test_valid_video(self):
        """
        Videos are very simple, they only need a video_link and title set.
        """
        self.client.login(**self.user_cred)
        response = self._post_video()

        # Video was created
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Video.objects.count(), 1)

        # The user is associated with the new content type and it's marked
        # as new. By default new content types are 'member only'.
        video = Video.objects.all()[0]
        self.assertEqual(video.submitted_by, self.user)
        self.assertEqual(video.status, Video.STATUS_CHOICES.new)
        self.assertEqual(video.permission, Video.PERMISSION_CHOICES.member)
