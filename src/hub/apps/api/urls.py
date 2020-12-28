from django.conf.urls import url

from .views import OrganizationsApiView, TagsApiView


urlpatterns = [
    url(
        r'^organizations/$',
        OrganizationsApiView.as_view(),
        name='organizations'),  # Filtered Topics
    url(r'^tags/$', TagsApiView.as_view(), name='tags_autocomplete'),
]
