from django.test import TestCase
from django.contrib.auth import get_user_model
from ..content.types.academic import AcademicProgram
from ..content.models import ContentType

User = get_user_model()


class WithUserSuperuserTestCase(TestCase):
    """
    Some base models/structure to create before doing actual tests.
    """
    def setUp(self):
        self.superuser_cred = {'username': 'superjoe', 'password': 'password'}
        self.superuser = User.objects.create_superuser(email='superuser@example.com', **self.superuser_cred)

        self.user_cred = {'username': 'joe', 'password': 'password'}
        self.user = User.objects.create_user(email='user@example.com', **self.user_cred)

        return super(WithUserSuperuserTestCase, self).setUp()


class ContentTypePermissionTestCase(WithUserSuperuserTestCase):
    """
    Test permission handling of content type detail pages.
    """
    def setUp(self):
        """
        Create a non-published, member only academic program. We don't set a
        status or permission here, the default values are already very
        restrictive:

            status = new
            permission = member only
        """
        self.ct = AcademicProgram.objects.create(title='My academic program')

        return super(ContentTypePermissionTestCase, self).setUp()

    def test_default_content_type_is_secure(self):
        """
        Check that the default values of a content types just created are secure
        by default.
        """
        self.assertEqual(self.ct.status, ContentType.STATUS_CHOICES.new)
        self.assertEqual(self.ct.permission, ContentType.PERMISSION_CHOICES.member)

    def test_default_content_type_is_not_listed(self):
        """
        A non-logged in user can't access the content type page even if he knows
        the url, since it's not published yet.
        """
        self.client.logout()
        response = self.client.get(self.ct.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_logged_in_user_nor_superuser_can_see_unpublished(self):
        """
        No logged-in users, not even super users can see a content type which
        was not yet published.
        """
        self.client.login(**self.user_cred)
        response = self.client.get(self.ct.get_absolute_url())
        self.assertEqual(response.status_code, 404)

        self.client.login(**self.superuser_cred)
        response = self.client.get(self.ct.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_default_content_type_published_visible_to_member_only(self):
        """
        A default content type which was published is only visible to
        members (superusers).
        """
        self.ct.status = self.ct.STATUS_CHOICES.published
        self.ct.save()

        # Not logged in
        self.client.logout()
        response = self.client.get(self.ct.get_absolute_url())
        self.assertEqual(response.status_code, 403)

        # Logged in but no member
        self.client.login(**self.user_cred)
        response = self.client.get(self.ct.get_absolute_url())
        self.assertEqual(response.status_code, 403)

        # Logged in and member/superuser
        self.client.login(**self.superuser_cred)
        response = self.client.get(self.ct.get_absolute_url())
        self.assertEqual(response.status_code, 200)
