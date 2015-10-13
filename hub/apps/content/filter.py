import django_filters as filters
import django_tables2 as tables

from .models import ContentType

class SearchResultFilter(filters.FilterSet):
    pass

class ContentTypesFilter(filters.FilterSet):
    """
    The base filter which works across all content types, using fields which
    they all share. Each content type might have its own, additional type
    defined in `content.types.*`.
    """
    created = filters.DateRangeFilter()

    class Meta:
        model = ContentType
        fields = (
            'topics',
            'organizations',
            'created',
        )

class TopicFilter(filters.FilterSet):
    created = filters.DateRangeFilter()

    class Meta:
        model = ContentType
        fields = (
            'content_type',
            'organizations',
            'created',
        )


class ContentTypesTable(tables.Table):
    title = tables.Column('Title')
    organizations = tables.Column('Organization')
    content_type = tables.Column('Content Type')
    created = tables.Column('Date', )
    topics = tables.Column('Sustainability Topics')

    class Meta:
        model = ContentType
        fields = ('title', 'organizations', 'content_type', 'created', 'topics')
        attrs = {'class': 'table'}

    def render_topics(self, *args, **kwargs):
        return 'foo'
