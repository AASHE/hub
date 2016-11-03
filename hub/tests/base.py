import warnings

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import management

from aashe.aasheauth.models import AASHEUser


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

        aashe_user = AASHEUser.objects.create(
            user=self.member,
            drupal_id=1,
            drupal_session_key="blah"
        )
        aashe_user.set_drupal_user_dict(
            {'roles': {'Member': 'Member'}})
        aashe_user.save()

        return super(WithUserSuperuserTestCase, self).setUp()

    # def login_member(self, **credentials):
    #     """
    #         Extends the base login functionality to ensure that member status
    #         is set, if the user is the self.member
    #     """
    #     success = self.client.login(**credentials)
    #     if success and credentials == self.member_cred:
    #         self.member.aasheuser.set_drupal_user_dict(
    #             {'roles': {'Member': 'Member'}})
    #         self.member.aasheuser.save()
    #     return success


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
