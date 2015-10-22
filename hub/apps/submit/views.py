from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, FormView
from django import forms


from ..content.models import ContentType, CONTENT_TYPES, CONTENT_TYPE_CHOICES
from .forms import BaseForm



class SubmitIndexView(TemplateView):
    pass

class SubmitFormView(FormView):
    template_name = 'browse/add/content_type.html'

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        model = CONTENT_TYPES[self.kwargs['ct']]
        return forms.modelform_factory(model, BaseForm, exclude=['id'])
