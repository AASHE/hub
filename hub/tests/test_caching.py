from __future__ import unicode_literals
from mock import patch
import django_cache_url
from haystack.management.commands import update_index

from django.conf import settings
from django.core import management
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.core.cache import caches
from django.db import connection, reset_queries
from django.test import override_settings
from django.utils.http import urlquote

from ..apps.content.models import ContentType
from ..apps.content.types.academic import AcademicProgram
from ..apps.metadata.models import SustainabilityTopic
from .base import WithUserSuperuserTestCase

"""
Test caching

Test the home page caching, by viewing the page and then checking
that the cache key exists.

Use the locmem
"""


@override_settings(CACHES={'default': django_cache_url.parse('locmem://hub_test')}, DEBUG=True)
# @override_settings(CACHES = {'default': django_cache_url.parse('pymemcached://127.0.0.1:11211')})
class GeneralCachingTestCase(WithUserSuperuserTestCase):
    """
    Test caching on verious pages
    """
    def setUp(self):
        """
        update the memcached path to use local memory for testing
        """
        
        self.topic = SustainabilityTopic.objects.create(
            name="First Topic", slug="first_topic")
        
        self.ct1 = AcademicProgram.objects.create(
            title='First Academic Program',
            status=ContentType.STATUS_CHOICES.published)
        self.ct1.topics.add(self.topic)
        self.ct1.save()
        
        self.ct2 = AcademicProgram.objects.create(
            title='Second Academic Program',
            status=ContentType.STATUS_CHOICES.new)
        self.ct2.topics.add(self.topic)
        self.ct2.save()
        
        self.cache = caches['default']
        
        self.url_home = reverse('home')
        self.url_topic = reverse(
            'browse:browse', kwargs={'topic': self.topic.slug})
        self.url_ct = reverse('browse:browse', kwargs={'ct': 'academicprogram'})
        self.url_search = '{}?search=academic'.format(reverse('browse:browse'))
        self.url_detail1 = reverse(
            'browse:view',
            kwargs={
                'ct': 'academicprogram',
                'id': self.ct1.id,
                'slug': self.ct1.slug})
        self.url_detail2 = reverse(
            'browse:view',
            kwargs={
                'ct': 'academicprogram',
                'id': self.ct2.id,
                'slug': self.ct2.slug})

        return super(GeneralCachingTestCase, self).setUp()
        
    def test_home_page_cache(self):
        """
        request the home page three times
        the response should be cached and the second topic not displayed until
        the cache is cleared
        """
        cache = caches['default']
        cache.clear()
        response = self.client.get(self.url_home)
        self.assertContains(response, "First Topic", status_code=200)
    
        # add a topic and test that the response doesn't update
        _topic = SustainabilityTopic.objects.create(
            name="Second Topic", slug="second_topic")
        response = self.client.get(self.url_home)
        self.assertNotContains(response, "Second Topic", status_code=200)
        
        # clear the cache and we should get a new one
        cache.clear()
        response = self.client.get(self.url_home)
        self.assertContains(response, "Second Topic", status_code=200)

    # def test_get_params(self):
    #     """
    #     do get params change the template cache key?
    #
    #     conclusion: no
    #     """
    #     pass
    
    def run_topic_toolkit_test(self):
        """
            Runs the topic toolkit test with the existing client
            to test different user types
        """
        cache = caches['default']

        self.ct2.status = ContentType.STATUS_CHOICES.new
        self.ct2.save()

        # a different cache key should be used for authenticated users
        reset_queries()
        response = self.client.get(self.url_topic)
        self.assertContains(response, '<strong>First Academic Program', status_code=200)
        self.assertNotContains(response, '<strong>Second Academic Program', status_code=200)
        uncached_request_query_count = len(connection.queries)

        # adding another resource won't change the cached value
        self.ct2.status = ContentType.STATUS_CHOICES.published
        self.ct2.save()
        
        # now a cached version should be rendered
        reset_queries()
        response = self.client.get(self.url_topic)
        self.assertContains(response, '<strong>First Academic Program', status_code=200)
        self.assertNotContains(response, '<strong>Second Academic Program', status_code=200)
        cached_request_query_count = len(connection.queries)

        # print "**Toolkit Caching"
        # print "Uncached Queries: %d" % uncached_request_query_count
        # print "Cached Queries: %d" % cached_request_query_count
        self.assertTrue(uncached_request_query_count > cached_request_query_count)
        
        cache.clear()
        response = self.client.get(self.url_topic)
        self.assertContains(response, '<strong>First Academic Program', status_code=200)
        self.assertContains(response, '<strong>Second Academic Program', status_code=200)

    def test_topic_toolkit_tab(self):
        """
            Toolkit tab: Template caching - varies on: auth
        """
        cache = caches['default']
        cache.clear()
        
        self.assertEqual(self.ct1.permission, ContentType.PERMISSION_CHOICES.member)
        self.assertEqual(self.ct1.status, ContentType.STATUS_CHOICES.published)
        
        # unauthenticated users
        self.client.logout()
        self.run_topic_toolkit_test()
        
        # now for an authenticated user
        self.client.login(**self.user_cred)
        self.run_topic_toolkit_test()

        # finally test with members
        self.client.login(**self.member_cred)
        self.run_topic_toolkit_test()
        
    def run_resources_test(self, url):
        """
            run the resources tab tests for various users and get params
        """
        cache = caches['default']
        
        self.ct2.status = ContentType.STATUS_CHOICES.new
        self.ct2.save()
        
        # update the search index
        management.call_command('update_index', verbosity=0)
        
        # get the uncached version
        reset_queries()
        response = self.client.get(url)
        self.assertContains(response, '1 result', status_code=200)
        uncached_request_query_count = len(connection.queries)

        # create a second resource; it shouldn't render
        self.ct2.status = ContentType.STATUS_CHOICES.published
        self.ct2.save()
        
        # update the search index
        management.call_command('update_index', verbosity=0)

        # get the cached version
        reset_queries()
        response = self.client.get(url)
        self.assertContains(response, '1 result', status_code=200)
        cached_request_query_count = len(connection.queries)

        # print "**Resources List Caching"
        # print "Uncached Queries: %d" % uncached_request_query_count
        # print "Cached Queries: %d" % cached_request_query_count
        self.assertTrue(uncached_request_query_count > cached_request_query_count)

        # now clear the cache and it should render
        cache.clear()
        response = self.client.get(url)
        self.assertContains(response, '2 results', status_code=200)
        
    def test_topic_resources_tab(self):
        """
            Resources tab: Queryset caching - varies on: GET params, auth
        
            test each user type with and without get params
        """
        cache = caches['default']
        cache.clear()

        self.client.logout()
        self.run_resources_test(self.url_topic)
        self.run_resources_test(
            "%s?content_type=academicprogram" % self.url_topic)
        
        self.client.login(**self.user_cred)
        self.run_resources_test(self.url_topic)
        self.run_resources_test(
            "%s?content_type=academicprogram" % self.url_topic)
        
        self.client.login(**self.member_cred)
        self.run_resources_test(self.url_topic)
        self.run_resources_test(
            "%s?content_type=academicprogram" % self.url_topic)
        
    def test_topic_stars_tab(self):
        """
            STARS tab: Template caching - varies on: none
        """
        cache = caches['default']
        cache.clear()
        
        # test the stars tab
        self.topic.stars_tab_content = "This is the STARS tab!!"
        self.topic.save()

        response = self.client.get(self.url_topic)
        self.assertContains(response, "This is the STARS tab!!", status_code=200)
        
        self.topic.stars_tab_content = "This is [not] the STARS tab!!"
        self.topic.save()
        response = self.client.get(self.url_topic)
        self.assertContains(response, "This is the STARS tab!!", status_code=200)
        
        cache.clear()
        response = self.client.get(self.url_topic)
        self.assertContains(response, "This is [not] the STARS tab!!", status_code=200)

    def test_topic_partners_tab(self):
        """
            Partners tab: Template caching - varies on: none
        """
        cache = caches['default']
        cache.clear()

        self.topic.name = "Curriculum"
        self.topic.scpd_rss_feed = \
            "http://aashe.org/sustainable-campus-partners-directory/rss/sustainability-topic/curriculum/"
        self.topic.save()

        response = self.client.get(self.url_topic)
        self.assertContains(response, "Curriculum Partners", status_code=200)

        self.topic.name = "Energy"
        self.topic.save()
        response = self.client.get(self.url_topic)
        self.assertContains(response, "Curriculum Partners", status_code=200)

        cache.clear()
        response = self.client.get(self.url_topic)
        self.assertContains(response, "Energy Partners", status_code=200)

        # Confirm that a broken RSS Feed link will not break the page
        cache.clear()
        self.topic.scpd_rss_feed = \
            "http://aashe.org/sustainable-campus-partners-directory/rss/sustainability-topic/topic-does-not-exist/"
        self.topic.save()
        response = self.client.get(self.url_topic)
        self.assertEqual(response.status_code, 200)

        self.topic.name = "First Topic"
        self.topic.save()

    def test_content_type_view(self):
        """
            The content-type view should vary on auth and get params
        """
        cache = caches['default']
        cache.clear()

        self.client.logout()
        self.run_resources_test(self.url_ct)
        self.run_resources_test(
            "%s?topics=first_topic" % self.url_ct)
        
        self.client.login(**self.user_cred)
        self.run_resources_test(self.url_ct)
        self.run_resources_test(
            "%s?topics=first_topic" % self.url_ct)
        
        self.client.login(**self.member_cred)
        self.run_resources_test(self.url_ct)
        self.run_resources_test(
            "%s?topics=first_topic" % self.url_ct)
            
    def test_search_view(self):
        """
            The content-type view should vary on auth and get params
        """
        cache = caches['default']
        cache.clear()

        self.client.logout()
        self.run_resources_test(self.url_search)
        self.run_resources_test(
            "%s&topics=first_topic" % self.url_search)

        self.client.login(**self.user_cred)
        self.run_resources_test(self.url_search)
        self.run_resources_test(
            "%s&topics=first_topic" % self.url_search)

        self.client.login(**self.member_cred)
        self.run_resources_test(self.url_search)
        self.run_resources_test(
            "%s&topics=first_topic" % self.url_search)
            
        # now test a really long key (> 250)
        self.ct1.description = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent
        rhoncus orci eget ex sodales porta. Sed tincidunt elit quam, at
        tristique purus commodo viverra. Nullam fermentum et ipsum quis
        egestas. Donec nec lorem ut ligula sodales volutpat. Duis tincidunt
        justo elit, quis venenatis nisi vehicula nec.
        """
        self.ct1.save()
        self.ct2.description = self.ct1.description
        self.ct2.save()

        long_search_url = '{}?search='.format(reverse('browse:browse'))
        long_search_url = "%s%s" % (long_search_url, urlquote(self.ct1.description))
        self.run_resources_test(long_search_url)
            
    def test_detail_view(self):
        """
        A resource should vary on superuser only
        """
        self.client.login(**self.member_cred)
        self.run_detail_view_test()
        
        self.client.login(**self.superuser_cred)
        self.run_detail_view_test()
        
    def run_detail_view_test(self):
        """
        View the resource. Change the title. Render shouldn't change.
        Clear cache. New title should display. Reset the title.
        """
        cache = caches['default']
        response = self.client.get(self.url_detail1)
        self.assertContains(response, '<h2>First Academic Program', status_code=200)

        # change the title
        self.ct1.title = 'Renamed Academic Program'
        self.ct1.save()

        # the render shouldn't change bceause it's cached
        response = self.client.get(self.url_detail1)
        self.assertContains(response, '<h2>First Academic Program', status_code=200)
        self.assertNotContains(response, '<h2>Renamed Academic Program', status_code=200)
        
        # another resources shouldn't be affected
        self.ct2.status = ContentType.STATUS_CHOICES.published
        self.ct2.save()
        response = self.client.get(self.url_detail2)
        self.assertContains(response, '<h2>Second Academic Program', status_code=200)

        # now clear the cache and it should render
        cache.clear()
        response = self.client.get(self.url_detail1)
        self.assertContains(response, '<h2>Renamed Academic Program', status_code=200)
        
        # reset title
        self.ct1.title = '<h2>First Academic Program'
        self.ct1.save()
