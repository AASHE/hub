from django.core import mail
import os

from ..apps.metadata.models import SustainabilityTopic
from django.core.urlresolvers import reverse
from django.conf import settings

from .base import WithUserSuperuserTestCase


class RequiredFieldsTestCase(WithUserSuperuserTestCase):
    """
    Test that content submission require the right fields to match the reqs
    https://docs.google.com/spreadsheets/d/1ADsnCZXKU1lhA4GHc2xhsY5ddLRi7kgvYJLSTHZKlmw/
    """
    def setUp(self):

        self.submission_types = [
            {
                'ct': 'academicprogram',
                'expected_fields': [
                    'topics', 'disciplines', 'organizations', 'program_type'
                ],
                'min_reqs': ['website']
            },
            {
                'ct': 'casestudy',
                'expected_fields': [
                    'topics', 'organizations', 'description', 'background',
                    'goals', 'implementation', 'timeline', 'financing',
                    'results', 'lessons_learned'
                ],
                'min_reqs': ['author']
            },
            {
                'ct': 'presentation',
                'expected_fields': [
                    'topics', 'organizations', 'conf_name', 'date'
                ],
                'min_reqs': ['author', 'file']
            },
            {
                'ct': 'material',  # course material
                'expected_fields': [
                    'topics', 'disciplines', 'organizations', 'material_type'
                ],
                'conditionally_required': ['website', 'file']
            },
            {
                'ct': 'outreachmaterial',  # outreach material
                'expected_fields': [
                    'topics', 'organizations',
                ],
                'conditionally_required': ['website', 'file', 'image']
            },
            {
                'ct': 'photograph',
                'expected_fields': [
                    'topics', 'organizations',
                ],
                'min_reqs': ['image', ]
            },
            {
                'ct': 'publication',
                'expected_fields': [
                    'topics', '_type'
                ],
                'min_reqs': ['author'],
                'conditionally_required': ['website', 'file']
            },
            {
                'ct': 'centerandinstitute',
                'expected_fields': [
                    'topics', 'disciplines', 'organizations'
                ],
                'min_reqs': ['website', ]
            },
            {
                'ct': 'tool',
                'expected_fields': [
                    'topics', 'organizations'
                ],
                'conditionally_required': ['website', 'file']
            },
            {
                'ct': 'video',
                'expected_fields': [
                    'topics', 'organizations'
                ],
                'min_reqs': ['website']
            },
        ]

        self.management_form_data = {
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

            'image-TOTAL_FORMS': 0,
            'image-INITIAL_FORMS': 0,
            'image-MIN_NUM_FORMS': 0,
            'image-MAX_NUM_FORMS': 5,
        }

        SustainabilityTopic.objects.create(name="Curriculum")
        SustainabilityTopic.objects.create(name="Research")

        return super(RequiredFieldsTestCase, self).setUp()

    def test_requirements(self):
        self.client.login(**self.user_cred)
        for sub in self.submission_types:

            url = reverse('submit:form', kwargs={'ct': sub['ct']})
            response = self.client.post(url, self.management_form_data)
            errors = response.context['document_form']._errors

            expected = sub['expected_fields']
            expected.append('title')  # title applies everywhere
            for f in sub['expected_fields']:
                self.assertTrue(f in errors.keys(), "%s not found in keys" % f)

            if 'min_reqs' in sub.keys():
                for min_req in sub['min_reqs']:
                    self.assertEqual(
                        response.context[
                            "%s_formset" % min_req]._non_form_errors[0],
                        u'Please submit 1 or more forms.'
                    )

            error_count = len(sub['expected_fields'])
            if 'conditionally_required' in sub.keys():
                error_count += 1
                for req in sub['conditionally_required']:
                    self.assertTrue(
                        req in errors['__all__'][0],
                        "%s in __all__ error" % req)

            # match the total error count
            self.assertEqual(error_count, len(errors.keys()), errors.keys())
