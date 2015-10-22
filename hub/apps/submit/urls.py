from django.conf.urls import url
from .views import SubmitIndexView, SubmitFormView

urlpatterns = [
    url(r'^$', SubmitIndexView.as_view(), name='new'),
    url(r'^(?P<ct>[\w\-]+)/$', SubmitFormView.as_view(), name='form'),
]
