from django.test import TestCase
from django.contrib.auth import get_user_model

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

        return super(WithUserSuperuserTestCase, self).setUp()
