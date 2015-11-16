from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse

from ..apps.browse.templatetags.browse_tags import permission_flag
from ..apps.content.models import ContentType
from ..apps.content.types.academic import AcademicProgram
from ..apps.metadata.models import SustainabilityTopic
from .base import WithUserSuperuserTestCase


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

class PermissionFlagTagTestCase(ContentTypePermissionTestCase):
    """
    The `permission_flag` template tag a little HTML widget that is
    rendered for publically listed resources, which the user has no
    access to.
    """
    # Strings the template tag returns for each permission state
    # The templatetag returns a HTML string so we can't easily compare against
    # a context object.
    MATCH_LOGIN_REQUIRED = 'Login Required'
    MATCH_MEMBER_REQUIRED = 'Membership Required'

    def test_permission_flag_unauthorized_user(self):
        """
        Unauthenticated users will see a flag according to the permission of
        each content type, either login or membership-requird.
        """
        # Open resources won't have a permission flag since they can be viewed
        # by anybody.
        self.ct.permission = self.ct.PERMISSION_CHOICES.open
        self.ct.save()
        self.assertEqual(permission_flag(self.ct, AnonymousUser()), None)

        # 'login required' resource has 'Login Required' in it's label
        self.ct.permission = self.ct.PERMISSION_CHOICES.login
        self.ct.save()
        self.assertTrue(self.MATCH_LOGIN_REQUIRED in permission_flag(self.ct, AnonymousUser()))

        # 'member required' resource has 'Membership Required' in it's label
        self.ct.permission = self.ct.PERMISSION_CHOICES.member
        self.ct.save()
        self.assertTrue(self.MATCH_MEMBER_REQUIRED in permission_flag(self.ct, AnonymousUser()))

    def test_permission_flag_for_logged_in_user(self):
        """
        Logged in users will only see a flag for content which requires
        membership.
        """
        self.client.login(**self.user_cred)

        self.ct.permission = self.ct.PERMISSION_CHOICES.open
        self.ct.save()
        self.assertEqual(permission_flag(self.ct, self.user), None)

        self.ct.permission = self.ct.PERMISSION_CHOICES.login
        self.ct.save()
        self.assertEqual(permission_flag(self.ct, self.user), None)

        self.ct.permission = self.ct.PERMISSION_CHOICES.member
        self.ct.save()
        self.assertTrue(self.MATCH_MEMBER_REQUIRED in permission_flag(self.ct, self.user))

    def test_permission_flag_for_membership_user(self):
        """
        Members won't see any flag at all.
        """
        self.client.login(**self.superuser_cred)

        self.ct.permission = self.ct.PERMISSION_CHOICES.open
        self.ct.save()
        self.assertEqual(permission_flag(self.ct, self.superuser), None)

        self.ct.permission = self.ct.PERMISSION_CHOICES.login
        self.ct.save()
        self.assertEqual(permission_flag(self.ct, self.superuser), None)

        self.ct.permission = self.ct.PERMISSION_CHOICES.member
        self.ct.save()
        self.assertEqual(permission_flag(self.ct, self.superuser), None)


class BrowsePermissionTestCase(WithUserSuperuserTestCase):
    """
    Test cases around the different permissions for the browse view
    (search results).

    - The homepage is open for all audiences
    - Search list browse results need auth
    - Topic list browse results need auth
    - Content Type browse results need auth
      - except certain 'PUBLIC_CONTENT_TYPES' content types
        which results are  open to unauthed users as well
    """
    def setUp(self):
        # Setup some content
        self.sus = SustainabilityTopic.objects.create(name='Research', slug='research')

        # URLs
        self.url_home = reverse('home')
        self.url_search = '{}?search=keyword'.format(reverse('browse:browse'))
        self.url_topic = reverse('browse:browse', kwargs={'topic': self.sus.slug})
        self.url_ct = reverse('browse:browse', kwargs={'ct': 'video'})

        return super(BrowsePermissionTestCase, self).setUp()

    def test_homepage_is_visible_to_all(self):
        """
        Homepage is visible to all users, no matter if authed or not.
        """
        self.client.logout()
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 200)

        self.client.login(**self.user_cred)
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 200)

        self.client.login(**self.superuser_cred)
        response = self.client.get(self.url_home)
        self.assertEqual(response.status_code, 200)

    def test_topic_view_is_auth_only(self):
        """
        Unauthed members can't see the topic view.
        """
        self.client.logout()
        response = self.client.get(self.url_topic)
        self.assertEqual(response.status_code, 403)

        self.client.login(**self.user_cred)
        response = self.client.get(self.url_topic)
        self.assertEqual(response.status_code, 200)

        self.client.login(**self.superuser_cred)
        response = self.client.get(self.url_topic)
        self.assertEqual(response.status_code, 200)

    def test_content_type_view_is_auth_only(self):
        """
        Unauthed members can't see the content type view.
        """
        self.client.logout()
        response = self.client.get(self.url_ct)
        self.assertEqual(response.status_code, 403)

        self.client.login(**self.user_cred)
        response = self.client.get(self.url_ct)
        self.assertEqual(response.status_code, 200)

        self.client.login(**self.superuser_cred)
        response = self.client.get(self.url_ct)
        self.assertEqual(response.status_code, 200)

    def test_open_ct_is_visible_to_anybody(self):
        """
        Certain, OPEN content types are visible to anybody.
        """
        if not settings.PUBLIC_CONTENT_TYPES:
            return
        open_url = reverse('browse:browse', kwargs={
            'ct': settings.PUBLIC_CONTENT_TYPES[0]})
        self.client.logout()
        response = self.client.get(open_url)
        self.assertEqual(response.status_code, 200)

    def test_search_view_is_auth_only(self):
        """
        Unauthed members can't see the search view.
        """
        self.client.logout()
        response = self.client.get(self.url_search)
        self.assertEqual(response.status_code, 403)

        self.client.login(**self.user_cred)
        response = self.client.get(self.url_search)
        self.assertEqual(response.status_code, 200)

        self.client.login(**self.superuser_cred)
        response = self.client.get(self.url_search)
        self.assertEqual(response.status_code, 200)
