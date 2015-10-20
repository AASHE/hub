from django.conf.urls import include, url
from django.contrib import admin

import hub.apps.browse.views as browse
import hub.apps.api.views as api

urlpatterns = [
    url(r'^$', browse.HomeView.as_view(), name='browse-home'),
    url(r'^browse/$', browse.BrowseView.as_view(), name='browse'),
    url(r'^browse/topics/(?P<topic>[\w\-]+)/$', browse.BrowseView.as_view(), name='browse'),
    url(r'^browse/types/(?P<ct>[\w\-]+)/$', browse.BrowseView.as_view(), name='browse'),

    url(r'^api/organizations/$', api.organizations),

    url(r'^admin/', include(admin.site.urls)),
]
