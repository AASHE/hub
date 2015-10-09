from django.views.generic import TemplateView
from django_tables2 import SingleTableView

from ..content.models import ContentType
from ..content.filter import ContentTypesFilter, ContentTypesTable, TopicFilter
from ..metadata.models import SustainabilityTopic


class BaseBrowseView(TemplateView):
    """
    """
    def get_context_data(self, **kwargs):
        ctx = super(BaseBrowseView, self).get_context_data(**kwargs)
        ctx.update({
            'topic_list': SustainabilityTopic.objects.all(),
            'content_type_list': dict(ContentType.CONTENT_TYPES),
        })
        return ctx


class HomeView(BaseBrowseView):
    """
    """
    template_name = 'home.html'


class ByTopicView(SingleTableView):
    template_name = 'topic.html'
    table_class = ContentTypesTable

    def get(self, *args, **kwargs):
        self.topic = SustainabilityTopic.objects.get(pk=self.kwargs['topic'])
        return super(ByTopicView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ByTopicView, self).get_context_data(**kwargs)
        ctx.update({
            'topic': self.topic,
        })
        return ctx

    def get_queryset(self):
        return TopicFilter(self.request.GET,
            queryset=ContentType.objects.filter())


class ByContentTypeView(SingleTableView):
    template_name = 'type.html'
    table_class = ContentTypesTable

    def get_context_data(self, **kwargs):
        ctx = super(ByContentTypeView, self).get_context_data(**kwargs)
        ctx.update({
            'type': dict(ContentType.CONTENT_TYPES)[self.kwargs['type']],
        })
        return ctx

    def get_queryset(self):
        return ContentTypesFilter(self.request.GET,
            queryset=ContentType.objects.filter(content_type=self.kwargs['type']))
