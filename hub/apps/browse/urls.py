from django.conf.urls import url

from .views import BrowseView, ResourceView


urlpatterns = [
    url(r'^$', BrowseView.as_view(), name='browse'),  # Search result
    url(r'^topics/(?P<topic>[\w\-]+)/$', BrowseView.as_view(), name='browse'),  # Filtered Topics
    url(r'^types/(?P<ct>[\w\-]+)/$', BrowseView.as_view(), name='browse'),  # Filterd Content Types

    # # Short detail url, not publically available
    url(r'^(?P<ct>[\w\-]+)/(?P<id>[\d]+)/$', ResourceView.as_view(), name='view'),

    # Long detial url, which is linked throughout the system
    url(r'^(?P<ct>[\w\-]+)/(?P<id>[\d]+)/(?P<slug>.*)$', ResourceView.as_view(), name='view'),
]
