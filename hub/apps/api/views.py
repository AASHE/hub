from __future__ import unicode_literals

from logging import getLogger

from django.core.cache import cache
from django.views.generic import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.template.defaultfilters import slugify

from ..metadata.models import Organization
from ..content.models import ContentType

logger = getLogger(__name__)


class BaseApiView(View):
    cache = False
    cache_timeout = 60 * 60

    def get(self, request, *args, **kwargs):
        """
        Respond the content of `self.get_data` as JSON. Cache it, if enabled.
        """
        if self.cache:
            data = cache.get(self.get_cache_key())
            if data:
                logger.debug('API response: cache hit :: {}'.format(
                    self.get_cache_key()))
                return data

        data = JsonResponse(self.get_data(), safe=False)

        if self.cache:
            logger.debug('API response: cache set :: {}'.format(
                self.get_cache_key()))
            cache.set(self.get_cache_key(), data, self.cache_timeout)

        return data


class AutoCompleteView(BaseApiView):

    def get(self, request, *args, **kwargs):
        """
        Store the `q` keyword in the class namespace.
        """
        if not self.request.GET.get('q'):
            return HttpResponseBadRequest('No search term given')
        self.q = self.request.GET['q']
        if len(self.q) < self.min_keyword_length:
            return HttpResponseBadRequest('Search term must be at least {} '
                'characters long.'.format(self.min_keyword_length))
        return super(AutoCompleteView, self).get(request, *args, **kwargs)


class OrganizationsApiView(AutoCompleteView):
    """
    Returns a list of organizations matching a given `q` keyword.
    """
    cache = True

    # API view specific
    max_num_results = 50
    min_keyword_length = 2

    def get_cache_key(self):
        return 'api_organizations_{}'.format(slugify(self.q))

    def get_data(self):
        data = (Organization.objects.values('pk', 'org_name')
            .filter(org_name__icontains=self.q))
        return list(data)


class TagsApiView(AutoCompleteView):
    """
    Returns a list of tags matching a given `q` keyword.
    """
    cache = True

    # API view specific
    max_num_results = 50
    min_keyword_length = 2

    def get_cache_key(self):
        return 'api_tags_{}'.format(slugify(self.q))

    def get_data(self):
        qs = ContentType.keywords.tag_model.objects.values('pk', 'name').distinct('name')
        # data = (Organization.objects.values('pk', 'org_name')
        qs = qs.filter(name__icontains=self.q)
        return list(qs)
