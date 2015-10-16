from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView

from ..content.models import ContentType
from ..metadata.models import SustainabilityTopic
from .filter import BrowseFilter

class HomeView(TemplateView):
    """
    The Home view.
    """
    template_name = 'browse/home.html'

    def get_context_data(self, **kwargs):
        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx.update({
            'topic_list': SustainabilityTopic.objects.all(),
            'content_type_list': dict(ContentType.CONTENT_TYPES),
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

    def get_template_names(self):
        """
        If a specific 'topic' is set in the url name, we'll render a template
        for this. In all other cases we have a generic browse result template.
        """
        topic = self.kwargs.get('topic')
        if topic:
            return (
                'browse/topics/{}.html'.format(topic),
                'browse/topics/generic.html'
            )
        return ('browse/results.html',)

    def get_queryset(self):
        return BrowseFilter(
            self.request.GET,
            queryset=ContentType.objects.all(),
            prefix='hf'
        )

    def get_context_data(self, **kwargs):
        ctx = super(BrowseView, self).get_context_data(**kwargs)
        ctx.update({
            'topic_list': SustainabilityTopic.objects.all(),
            'content_type_list': dict(ContentType.CONTENT_TYPES),
        })
        return ctx
