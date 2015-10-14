from django.conf.urls import include, url
from django.contrib import admin

import hub.apps.browse.views as browse
import hub.apps.api.views as api

urlpatterns = [
    url(r'^$', browse.HomeView.as_view(), name='browse-home'),
    url(r'^by-topic/(?P<topic>[\w\-]+)/$', browse.ByTopicView.as_view(), name='browse-topic'),
    url(r'^by-type/(?P<type>[\w\-]+)/$', browse.ByContentTypeView.as_view(), name='browse-type'),

    url(r'^api/organizations/$', api.organizations),

    url(r'^admin/', include(admin.site.urls)),
]
