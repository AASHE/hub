from __future__ import unicode_literals

from logging import getLogger

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import ObjectDoesNotExist
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, TemplateView
from ratelimit.mixins import RatelimitMixin

from ...permissions import get_aashe_member_flag
from ..content.models import CONTENT_TYPES, ContentType
from ..metadata.models import SustainabilityTopic, SustainabilityTopicFavorite

from tagulous.views import autocomplete

import feedparser
from django.utils.text import slugify

from django.db.models import Count, F, CharField, Value as V
from django.db.models.functions import Concat
from django.utils.safestring import mark_safe
from django.db.models import Q

logger = getLogger(__name__)


class HomeView(TemplateView):
    """
    The Home view.

    @permisson: HomeView is visible for everybody
    """
    template_name = 'browse/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx.update({
            'topic_list': SustainabilityTopic.objects.all(),
            'content_type_list': CONTENT_TYPES,
        })
        return ctx


class BrowseView(RatelimitMixin, ListView):
    """
    A very generic browse view to handle all sorts of views at once. Generally
    we have two views:

        - browse view, handling the result set for keyword and content type
          searches

        - topic view, if a topic is set, we render a custom template located
          in `browse/topic/<name>.html`.

    @permission: BrowseView generally requires Login, except:

        - The AcademicProgram content type view is open
        - The Toolkit tab is open, all others not visible
    """
    template_name = 'browse/browse.html'
    content_type_class = None
    sustainabilty_topic = None
    paginate_by = 50
    filterset_form = None

    # Rate-limiting
    ratelimit_key = 'ip'
    ratelimit_rate = settings.BROWSE_RATE_LIMIT
    ratelimit_block = True
    ratelimit_method = 'GET'

    def dispatch(self, *args, **kwargs):
        """
        Persmission handling and load some generic objects into the class so we
        have it globally available.
        """
        # Load the specified SustainabilityTopic
        if self.kwargs.get('topic'):
            self.sustainabilty_topic = get_object_or_404(
                SustainabilityTopic, slug=self.kwargs['topic'])

        # Load the specified Content Type object. Make Content Type a nice
        # little object so it works similar to SustainabilityTopic
        if self.kwargs.get('ct'):
            if self.kwargs.get('ct') not in CONTENT_TYPES:
                raise Http404('This Content type does not exist')
            self.content_type_class = CONTENT_TYPES[self.kwargs['ct']]
            self.content_type_class.slug = self.kwargs.get('ct')

        # If no content type and no topic is set, we need at least a
        # search keyword or organization:
        if (
            not self.sustainabilty_topic and
            not self.content_type_class and
            'search' not in self.request.GET and
            'organizations' not in self.request.GET and
            'tagfilter' not in self.request.GET
        ):
            return HttpResponseRedirect(reverse('home'))

        return super(BrowseView, self).dispatch(*args, **kwargs)

    def get_template_names(self):
        """
        If a specific 'topic' is set in the url name, we'll render a template
        for this. In all other cases we have a generic browse result template.
        """
        if self.sustainabilty_topic:
            return ('browse/results/topic.html',)

        if self.content_type_class:
            return ('browse/results/content_type.html',)

        return ('browse/results/search.html',)

    def get_filterset(self):
        """
        Builds and returns a filter form object. Content Type classes might
        have their own, custom FilterSet defined in
        `model.get_custom_filterset`.
        """
        # GenericFilterSet imported here to avoid early execution of __init__
        # methods on filters @todo - keep an eye on performance
        from .filterset import GenericFilterSet
        if (
            self.content_type_class and
            hasattr(self.content_type_class, 'get_custom_filterset')
        ):
            return self.content_type_class.get_custom_filterset()
        else:
            return GenericFilterSet

    def get_filterset_data(self):
        """
        Whether we're in a content type or topic view, we want to have the list
        of content types already filtered by these.
        """
        data = self.request.GET.copy()
        if self.sustainabilty_topic:
            data['topics'] = self.sustainabilty_topic.slug
        if self.content_type_class:
            data['content_type'] = self.content_type_class.slug
        return data

    def get_title(self):
        """
        Returns the actual title of the current object, either topic,
        content type or search.
        """
        if self.sustainabilty_topic:
            return self.sustainabilty_topic.name
        if self.content_type_class:
            return self.content_type_class._meta.verbose_name_plural
        if self.request.GET.get('search'):
            return 'Search for "{}"'.format(self.request.GET['search'])
        return 'Search Results'

    def get_queryset(self):
        """
        Normally a filterset would be a FilterSet object, where its iterator
        runs over the integrated queryset, so it pretty much acts like a
        regular queryset. The downside is that we can't run pagination/sorting
        on this filterset, like we'd do on a regular filterset. Therefor we
        transform it back, and only return the actual queryset, while we put
        the attached filter-form aside and load it separately into context.
        """
        filterset = self.get_filterset()(
            self.get_filterset_data(),
            queryset=ContentType.objects.published())
        # Load form into class, bring it back below in context.
        self.filterset_form = filterset.form
        return filterset.qs.distinct()

    def get_cache_key(self):
        """
        Generates a cache key based on:
            - url
            - anon/auth/member user status
            - get params

        Note: memcached limits keys to 250 characters
        """

        key = self.request.path

        if self.request.user.is_authenticated():
            if hasattr(self.request.user, 'aasheuser'):
                key = "%s[mem-%s]" % (
                    key, self.request.user.aasheuser.is_member())
            else:
                # usually just during testing
                key = "%s[mem-False]" % key
        else:
            key = "%s[anon]" % key

        key = "%s?" % key

        # sort the keys alphabetically for consistency
        keys_list = self.request.GET.keys()
        for k in keys_list:
            v = self.request.GET.getlist(k)
            if v and v != [u'']:
                v.sort()
                key = "%s&%s=%s" % (key, k, "/".join(v))

        if len(key) >= 250:
            # memcache limit of 250 characters - hash the long ones
            import hashlib
            hashed_key = hashlib.sha224(key).hexdigest()
            return hashed_key
        return key

    def get_context_data(self, **kwargs):
        ctx = super(BrowseView, self).get_context_data(**kwargs)
        topic_name = self.sustainabilty_topic.__str__()
        ctx.update({
            'object_list_form': self.filterset_form,
            'topic': self.sustainabilty_topic,
            'topic_name': topic_name,
            'topic_slug': slugify(topic_name),
            'topic_list': SustainabilityTopic.objects.all(),
            'content_type': self.content_type_class,
            'content_type_list': CONTENT_TYPES,
            'page_title': self.get_title(),
            'content_type_slug': self.kwargs.get('ct'),
            'cache_key': self.get_cache_key(),
        })

        # Additional toolkit content for topic views
        if self.sustainabilty_topic:
            featured_ids = SustainabilityTopicFavorite.objects.filter(
                topic=self.sustainabilty_topic).order_by(
                    'order').values_list('ct', flat=True)
            featured_content_types = ContentType.objects.published()
            featured_content_types = featured_content_types.filter(
                id__in=featured_ids)
            new_resources = ContentType.objects.published().filter(
                topics=self.sustainabilty_topic).order_by('-published')

            # @DONE - using the [:#] notation executes the query and undoes
            # caching. This needed to happen in the template `use |slice:":#"`

            news_list = self.sustainabilty_topic.get_rss_items()

            ctx.update({
                'featured_list': featured_content_types,
                'news_list': news_list,
                'new_resources_list': new_resources,
            })

            # Additional Partners Tab content for topic views
            try:
                rss_topic_feed = feedparser.parse(
                    self.sustainabilty_topic.scpd_rss_feed)
                if 'entries' in rss_topic_feed:
                    ctx.update({
                        'feed': rss_topic_feed,
                    })
            except Exception as e:  # Any error is bad here, catch all.
                logger.error('Feed parse failed; {}'.format(feed_address))
                logger.exception(e)

        # Additional Summary content for content type views
        if self.content_type_class:
            # Query all resources in this content type
            # and sort by date of publication
            new_resources = ContentType.objects.published()\
                .filter(content_type=self.content_type_class.slug)\
                .order_by('-published')

            # Count unique organizations in this data set
            orgs = new_resources\
                .values('organizations__account_num')\
                .distinct()

            # Count unique countries appearing within these organizations
            country_counts = new_resources\
                .values('organizations__country')\
                .annotate(count=Count('organizations__account_num'))\
                .order_by()

            # Count unique states appearing within these organizations that
            # have country=USA
            state_counts = new_resources\
                .filter(organizations__country_iso='US')\
                .values('organizations__state')\
                .annotate(count=Count('organizations__account_num')).order_by()

            # Count unique states appearing within these organizations
            # that have country=Canada
            province_counts = new_resources\
                .filter(organizations__country_iso='CA')\
                .values('organizations__state')\
                .annotate(count=Count('organizations__account_num')).order_by()

            # Count unique topics associated with these pieces of content
            # output a dict of pairs of names and counts
            topic_counts = [
                {
                    'name'.encode("utf8"): t['topics__name'].encode("utf8"),
                    'count'.encode("utf8"): t['count'],
                    'link'.encode("utf8"): t['link'].encode("utf8")
                }
                for t in
                new_resources.values('topics__name')
                .annotate(count=Count('id')).order_by('-count')
                .annotate(
                    link=Concat(
                        V("/browse/types/"),
                        V(self.content_type_class.slug),
                        V("/?search=&content_type="),
                        V(self.content_type_class.slug),
                        V("&topics="),
                        'topics__slug',
                        V("&country=#resources-panel"),
                        output_field=CharField()
                    )
                )
            ]

            # Count unique academic disciplines associated with these pieces
            # of content and output a dict of pairs of names and counts
            discipline_counts = new_resources.values('disciplines__name')\
                .annotate(count=Count('id')).order_by('-count')

            # Get data for the map
            map_data = [
                [t[0].encode("utf8"), float(t[1]), float(t[2]), t[3],
                 t[4], t[5].encode("utf8")]
                for t in
                new_resources.exclude(Q(organizations__org_name=None))
                             .exclude(Q(organizations__latitude=''))
                             .values_list('organizations__org_name',
                                          'organizations__latitude',
                                          'organizations__longitude',
                                          'organizations__account_num',
                                          )
                             .annotate(
                                    count=Count('organizations__account_num')
                             ).annotate(
                                    link=Concat(
                                        V("/browse/types/"),
                                        V(self.content_type_class.slug),
                                        V("/?search=&content_type="),
                                        V(self.content_type_class.slug),
                                        V("&organizations="),
                                        str('organizations__account_num'),
                                        V("&country=#resources-panel"),
                                        output_field=CharField()
                                    )
                             ).order_by()
                        ]

            # Add all of this to the context data
            ctx.update({
                'new_resources_list': new_resources,
                'orgs': orgs,
                'country_counts': country_counts,
                'state_counts': state_counts,
                'province_counts': province_counts,
                'topic_counts': topic_counts,
                'topic_counts_safe': mark_safe(topic_counts),
                'discipline_counts': discipline_counts,
                'map_data': mark_safe(map_data),
                'GOOGLE_API_KEY': settings.GOOGLE_API_KEY,
            })
        return ctx


class ResourceView(DetailView):
    """
    Actual Detail view of ContentType objects.

    @permisson:

        - Login Required
        - Each ContentType has a `member_only` attribut we will check too.
          Some objects might only need Login.
    """
    def dispatch(self, *args, **kwargs):
        """
        Check if this object is `Member Only`. If so, only AASHE members and
        Auth superusers are able to see it.

        Other than that, at least a login is required, which is provided by
        the `LoginRequiredMixin`.
        """
        obj = self.get_object()

        # Check if this object is open to anybody
        if obj.permission == ContentType.PERMISSION_CHOICES.open:
            return super(ResourceView, self).dispatch(*args, **kwargs)

        # The user needs to be at least logged in from here
        if not self.request.user.is_authenticated():
            return render(
                self.request,
                'registration/login_required.html',
                status=HttpResponseForbidden.status_code)

        # If the object only needs login, we're fine and can display it:
        if obj.permission == ContentType.PERMISSION_CHOICES.login:
            return super(ResourceView, self).dispatch(*args, **kwargs)

        # User is either member, or superuser, so its' fine to view
        if get_aashe_member_flag(self.request.user):
            return super(ResourceView, self).dispatch(*args, **kwargs)

        # Otherwise, and finally, we deny.
        return render(
            self.request,
            'registration/member_required.html',
            status=HttpResponseForbidden.status_code)

    def get_template_names(self):
        return (
            'browse/details/{}.html'.format(self.kwargs['ct']),
            'browse/details/base.html'
        )

    def get_object(self, queryset=None):
        if not self.kwargs['ct'] in CONTENT_TYPES:
            raise Http404('Resource model does not exist')
        try:
            ct_model = CONTENT_TYPES[self.kwargs['ct']]
            obj = ct_model.objects.get(
                status=ContentType.STATUS_CHOICES.published,
                pk=self.kwargs['id']
            )
        except ObjectDoesNotExist:
            raise Http404('Resource not found')
        return obj

    def get_context_data(self, **kwargs):
        ctx = super(ResourceView, self).get_context_data(**kwargs)
        ctx.update({
            'label_overrides': self.object.label_overrides(),
        })
        return ctx


def autocomplete_tags(request):
    """
        The tags autocomplete view
    """
    return autocomplete(
        request,
        ContentType.tags.tag_model.objects.all().distinct()
    )
