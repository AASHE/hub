from logging import getLogger

from django.http import Http404
from django.views.generic import TemplateView, FormView
from django import forms
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory, formset_factory

from ...permissions import LoginRequiredMixin
from ..content.models import CONTENT_TYPES, CONTENT_TYPE_CHOICES, Author
from .forms import SubmitResourceForm, AuthorForm

logger = getLogger(__name__)


class SubmitIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'submit/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(SubmitIndexView, self).get_context_data(**kwargs)
        ctx.update({
            'content_type_list': dict(CONTENT_TYPE_CHOICES),
        })
        return ctx

class SubmitFormView(LoginRequiredMixin, FormView):
    template_name = 'submit/form.html'

    def dispatch(self, *args, **kwargs):
        if self.kwargs.get('ct') not in CONTENT_TYPES:
            raise Http404('This Content type does not exist')
        self.content_type_class = CONTENT_TYPES[self.kwargs['ct']]
        self.content_type_class.slug = self.kwargs.get('ct')
        return super(SubmitFormView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return reverse('submit:thank-you')

    def get_context_data(self, **kwargs):
        ctx = super(SubmitFormView, self).get_context_data(**kwargs)
        ctx.update({
            'content_type_label': self.content_type_class._meta.verbose_name,
            'author_formset': formset_factory(AuthorForm, min_num=0, max_num=3, extra=3),
        })
        return ctx

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.
        """
        model = self.content_type_class
        form = forms.modelform_factory(model, SubmitResourceForm)
        return form(**self.get_form_kwargs())

    def form_valid(self, form):
        self.object = form.save(self.request)
        return super(SubmitFormView, self).form_valid(form)
