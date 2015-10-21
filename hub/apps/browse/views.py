from logging import getLogger

from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, FormView, DetailView
from django import forms

from ..content.models import ContentType, CONTENT_TYPES, CONTENT_TYPE_CHOICES
from ..metadata.models import SustainabilityTopic
from .filter import GenericFilterSet


logger = getLogger(__name__)


class HomeView(TemplateView):
    """
    The Home view.
    """
    template_name = 'browse/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx.update({
            'topic_list': SustainabilityTopic.objects.all(),
            'content_type_list': dict(CONTENT_TYPE_CHOICES),
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
    """
    template_name = 'browse/browse.html'
    content_type_class = None
    sustainabilty_topic = None

    def get(self, *args, **kwargs):
        """
        Load some generic objects into the class so we have it globally
        available.
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

        return super(BrowseView, self).get(*args, **kwargs)

    def get_template_names(self):
        """
        If a specific 'topic' is set in the url name, we'll render a template
        for this. In all other cases we have a generic browse result template.
        """
        return self.sustainabilty_topic \
            and ('browse/results/topic.html',) \
             or ('browse/results/other.html',)

    def get_filterset(self):
        """
        Builds and returns a filter form object. Content Type classes might
        have their own, custom FilterSet defined in `model.get_custom_filterset`.
        """
        if self.content_type_class and hasattr(
        self.content_type_class, 'get_custom_filterset'):
            return self.content_type_class.get_custom_filterset()
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
        logger.debug('filterset data: {}'.format(data))
        return data

    def get_title(self):
        """
        Returns the actual title of the current object, either topic,
        content type or search.
        """
        if self.sustainabilty_topic:
            return self.sustainabilty_topic.name
        if self.content_type_class:
            return self.content_type_class._meta.verbose_name
        if self.request.GET.get('search'):
            return 'Your Search for "{}"'.format(self.request.GET['search'])
        return 'Your Search Results'

    def get_queryset(self):
        return self.get_filterset()(
            self.get_filterset_data(),
            queryset=ContentType.objects.published())

    def get_context_data(self, **kwargs):
        ctx = super(BrowseView, self).get_context_data(**kwargs)
        ctx.update({
            'topic': self.sustainabilty_topic,
            'topic_list': SustainabilityTopic.objects.all(),
            'content_type': self.content_type_class,
            'content_type_list': dict(CONTENT_TYPE_CHOICES),
            'page_title': self.get_title(),
        })
        return ctx


class BaseForm(forms.ModelForm):
    pass

class AddContentTypeView(FormView):
    template_name = 'browse/add/content_type.html'

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        model = CONTENT_TYPES[self.kwargs['ct']]
        return forms.modelform_factory(model, BaseForm, exclude=['id'])


class ViewResource(DetailView):
    queryset = ContentType.objects.published()

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            obj = self.get_object()
            if obj.member_only:
                return HttpResponseForbidden('Member Only')
        return super(ViewResource, self).get(*args, **kwargs)


    def get_template_names(self):
        return (
            'browse/details/{}.html'.format(self.kwargs['ct']),
            'browse/details/base.html'
        )

    def get_object(self, queryset=None):
        if not self.kwargs['ct'] in CONTENT_TYPES:
            raise Http404('Resource model does not exist')

        if queryset is None:
            queryset = self.get_queryset()

        try:
            ct_model = CONTENT_TYPES[self.kwargs['ct']]
            obj = ct_model.objects.get(pk=self.kwargs['id'])
        except queryset.model.DoesNotExist:
            raise Http404('Resource not found')
        return obj
