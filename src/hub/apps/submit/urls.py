from django.conf.urls import url
from .views import SubmitIndexView, SubmitFormView

urlpatterns = [
    url(r'^$', SubmitIndexView.as_view(), name='new'),
    url(r'^thank-you/$', SubmitIndexView.as_view(
        template_name='submit/thank_you.html'), name='thank-you'),
    url(r'^(?P<ct>[\w\-]+)/$', SubmitFormView.as_view(), name='form'),
]
