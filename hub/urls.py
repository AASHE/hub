from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from aashe.aasheauth.views import login, logout

from hub.apps.browse.views import HomeView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^browse/', include('hub.apps.browse.urls', namespace='browse')),
    url(r'^submit-resource/', include('hub.apps.submit.urls', namespace='submit')),

    url(r'^api/v1/', include('hub.apps.api.urls', namespace='api')),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        url(r'^404$', 'django.views.defaults.page_not_found'),
        url(r'^500$', 'django.views.defaults.server_error'),
    ]
