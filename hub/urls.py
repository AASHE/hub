from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

import hub.apps.browse.views as browse
import hub.apps.api.views as api

urlpatterns = [
    url(r'^$', browse.HomeView.as_view(), name='browse-home'),
    url(r'^browse/$', browse.BrowseView.as_view(), name='browse'),
    url(r'^browse/topics/(?P<topic>[\w\-]+)/$', browse.BrowseView.as_view(), name='browse'),
    url(r'^browse/types/(?P<ct>[\w\-]+)/$', browse.BrowseView.as_view(), name='browse'),

    url(r'^add/(?P<ct>[\w\-]+)/$', browse.AddContentTypeView.as_view(), name='add'),

    url(r'^view/(?P<ct>[\w\-]+)/(?P<id>[\d]+)/$', browse.ViewResource.as_view(), name='view'),

    url(r'^api/organizations/$', api.organizations),

    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^admin/', include(admin.site.urls)),
]
