from django.test import TestCase
from django.contrib.auth import get_user_model

from django_membersuite_auth.models import MemberSuitePortalUser


User = get_user_model()


class WithUserSuperuserTestCase(TestCase):
    """
    Some base models/structure to create before doing actual tests.
    """
    def setUp(self):
        self.superuser_cred = {'username': 'superjoe', 'password': 'password'}
        self.superuser = User.objects.create_superuser(
            first_name='Jon',
            last_name='Doe',
            email='superuser@example.com',
            **self.superuser_cred
        )

        self.user_cred = {'username': 'joe', 'password': 'password'}
        self.user = User.objects.create_user(
            first_name='Jonny',
            last_name='Doey',
            email='user@example.com',
            **self.user_cred
        )

        self.member_cred = {'username': 'member', 'password': 'password'}
        self.member = User.objects.create_user(
            first_name='Jonny',
            last_name='Member',
            email='member@example.com',
            **self.member_cred
        )

        MemberSuitePortalUser.objects.create(user=self.member,
                                             membersuite_id=1,
                                             is_member=True)

        return super(WithUserSuperuserTestCase, self).setUp()


# The kwargs required for `create` for each content type
EXTRA_REQUIRED_CT_KWARGS = {
    'casestudy': {
        'background': "blah",
        'goals': "blah",
        'implementation': "blah",
        'timeline': "blah",
        'financing': "blah",
        'results': "blah",
        'lessons_learned': "blah",
        'consider_for_award': False,
    },
}
