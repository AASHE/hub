import django.views.defaults
import django_admin_blocks
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from ratelimit.decorators import ratelimit

from .apps.browse.views import HomeView
from aashe.aasheauth.views import login, logout


django_admin_blocks.autodiscover()

urlpatterns = [

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^browse/', include('hub.apps.browse.urls', namespace='browse')),
    url(r'^submit-resource/',
        include('hub.apps.submit.urls', namespace='submit')),

    url(r'^api/v1/', include('hub.apps.api.urls', namespace='api')),

    # url(r'^login/$', login, name='login'),
    url(r'^login/$',
        ratelimit(
            key='post:username',
            rate=settings.LOGIN_RATE_LIMIT,
            block=True)(login),
        name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^_ad/', include(admin.site.urls)),

    # Link checking url pattern
    url(r'^_ad/linkcheck/', include('linkcheck.urls')),
    url(r'^s3direct/', include('s3direct.urls')),

    # Let's Encrypt (django-acme-challenge)
    url(r'^.well-known/acme-challenge/', include('acme_challenge.urls')),

    url(r'^', include('django.contrib.flatpages.urls')),
]

if settings.DEBUG:  # pragma: no cover
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        url(r'^404$', django.views.defaults.page_not_found),
        url(r'^500$', django.views.defaults.server_error),
    ]
