from logging import getLogger

from django.http import Http404, HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django import forms
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory

from ...permissions import LoginRequiredMixin
from ..content.models import CONTENT_TYPES, CONTENT_TYPE_CHOICES
from .forms import AuthorForm, SubmitResourceForm

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

    def get(self, request, *args, **kwargs):
        forms = self.get_form()
        return self.render_to_response(self.get_context_data(**forms))

    def post(self, request, *args, **kwargs):
        """
        Handle POST of multiple files.
        """
        forms = self.get_form()
        document_form, author_formset = forms.values()

        if document_form.is_valid() and author_formset.is_valid():
            instance = document_form.save(self.request)
            for form in author_formset:
                form.save(instance=instance)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(**forms))

    def get_success_url(self):
        return reverse('submit:thank-you')

    def get_context_data(self, **kwargs):
        ctx = super(SubmitFormView, self).get_context_data(**kwargs)
        ctx.update({
            'content_type_label': self.content_type_class._meta.verbose_name,
        })
        return ctx

    def get_form(self, form_class=None):
        """
        Collection of our base DocumentForm and all related formsets.
        """
        DocumentForm = forms.modelform_factory(
            self.content_type_class,
            SubmitResourceForm)

        AuthorFormset = formset_factory(AuthorForm, max_num=3, extra=3)

        document_form = DocumentForm(prefix='document', **self.get_form_kwargs())
        author_formset = AuthorFormset(prefix='authors', **self.get_form_kwargs())

        return {
            'document_form': document_form,
            'author_formset': author_formset,
        }

    def get_form_kwargs(self, **kwargs):
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs
