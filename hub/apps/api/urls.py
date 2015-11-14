from django.conf.urls import url

from .views import OrganizationsApiView


urlpatterns = [
    url(r'^organizations/$', OrganizationsApiView.as_view(), name='organizations'),  # Filtered Topics
]
