from __future__ import unicode_literals

from logging import getLogger

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import ObjectDoesNotExist
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, TemplateView

from ...permissions import get_aashe_member_flag
from ..content.models import CONTENT_TYPES, ContentType
from ..metadata.models import SustainabilityTopic, SustainabilityTopicFavorite
from .filterset import GenericFilterSet

from tagulous.views import autocomplete

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


class BrowseView(ListView):
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

        # Search results do generally need LoginRequired, however there
        # are certain ContentTypes defined in PUBLIC_CONTENT_TYPES which
        # don't even need login, they are browseable by everyone.
        if (
            self.content_type_class and
            self.content_type_class.slug in settings.PUBLIC_CONTENT_TYPES
        ):
            return super(BrowseView, self).dispatch(*args, **kwargs)

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
        if (
            self.content_type_class and
            hasattr(self.content_type_class, 'get_custom_filterset')
        ):
            return self.content_type_class.get_custom_filterset()
        else:
            return GenericFilterSet

    def get_filterset_data(self):
        """
        Wether we're in a content type or topic view, we want to have the list
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
                key = "%s[mem-%s]" % (key, self.request.user.aasheuser.is_member())
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
        """
        The context can be cached based on three keys:
            - url
            - anon/auth/member user status
            - get params
        """
        ctx = super(BrowseView, self).get_context_data(**kwargs)
        ctx.update({
            'object_list_form': self.filterset_form,
            'topic': self.sustainabilty_topic,
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
            featured_content_types = featured_content_types.filter(id__in=featured_ids)
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
