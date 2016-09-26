from logging import getLogger

from django import forms
from django.core.urlresolvers import reverse
from django.forms.models import formset_factory
from django.http import Http404, HttpResponseRedirect
from django.views.generic import FormView, TemplateView

from ...permissions import LoginRequiredMixin
from ..content.models import CONTENT_TYPES, Author
from ..metadata.models import Organization
from .forms import AuthorForm, FileForm, ImageForm, SubmitResourceForm, \
    WebsiteForm

logger = getLogger(__name__)


class SubmitIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'submit/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(SubmitIndexView, self).get_context_data(**kwargs)
        ctx.update({
            'content_type_list': CONTENT_TYPES,
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

        # Validate the form and formsets
        valid = True
        for key, form in forms.items():
            if not form.is_valid():
                valid = False

        # Validate conditionally_required
        meets_reqs = self.validate_conditional_requirements(forms)

        if valid and meets_reqs:
            instance = forms['document_form'].save(self.request)
            # Save formsets
            formset_keys = [
                'author_formset', 'file_formset', 'image_formset',
                'website_formset'
            ]
            for key in formset_keys:
                if key in forms.keys():
                    for form in forms[key]:
                        if form.has_changed():
                            form.save(instance=instance)

            instance.create_thumbnails()

            return HttpResponseRedirect(self.get_success_url())

        ctx = self.get_context_data(**forms)
        ctx.update({'errors': True})
        return self.render_to_response(ctx)

    def get_success_url(self):
        return reverse('submit:thank-you')

    def get_context_data(self, **kwargs):
        ctx = super(SubmitFormView, self).get_context_data(**kwargs)

        # Create a template author form for the submitting user
        if 'author_formset' in kwargs.keys():
            ctx.update({
                'user_is_author_form': self.get_author_form_template(**kwargs)
            })

        ctx.update({
            'content_type_label': self.content_type_class._meta.verbose_name,
            'label_overrides': self.content_type_class.label_overrides(),
            'content_type_class': self.content_type_class,
            'content_type_slug': self.content_type_class.slug,
        })
        return ctx

    def get_form(self, form_class=None):
        """
        Collection of our base DocumentForm and all related formsets.
        """
        # The base 'document' form
        DocumentForm = forms.modelform_factory(
            self.content_type_class,
            SubmitResourceForm)

        # If the content type provides label overrides, update them
        labels = self.content_type_class.label_overrides()
        for field, label in labels.items():
            if field in DocumentForm.base_fields:
                DocumentForm.base_fields[field].label = label

        # If the content type provides required overrides, update them
        for field in self.content_type_class.required_field_overrides():
            if field in DocumentForm.base_fields:
                DocumentForm.base_fields[field].required = True

        # If the content type provides fields to be exluded, exclude them
        for field in self.content_type_class.exclude_form_fields():
            if field in DocumentForm.base_fields:
                del DocumentForm.base_fields[field]

        # If the content type has required topics
        initial_topics = self.content_type_class.preset_topics()
        if len(initial_topics) > 0:
            DocumentForm.base_fields['topics'].initial = initial_topics

        document_form = DocumentForm(
            prefix='document', **self.get_form_kwargs())

        # Additional formsets
        ctx = self.get_required_formsets()
        ctx['document_form'] = document_form
        return ctx

    def get_form_kwargs(self, **kwargs):
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get_author_form_template(self, **kwargs):
        f = kwargs['author_formset'].empty_form
        org = None
        if hasattr(self.request.user, 'aasheuser'):
            drupal_dict = self.request.user.aasheuser.get_drupal_user_dict()
            org = drupal_dict['profile_instlist']
            if type(org) is list:
                org = org[0]
            f.fields['organization'].initial = org
            f.fields['title'].initial = drupal_dict['profile_jobtitle']
        f.fields['name'].initial = self.request.user.get_full_name()
        f.fields['email'].initial = self.request.user.email
        return f

    def get_required_formsets(self):
        required_metadata = self.content_type_class.required_metadata()
        ctx = {}
        formset_pairs = [
            ('author', AuthorForm),
            ('image', ImageForm),
            ('file', FileForm),
            ('website', WebsiteForm)
        ]

        for key, formKlass in formset_pairs:
            if key in required_metadata.keys():
                formsetKlass = formset_factory(
                    formKlass,
                    min_num=required_metadata[key]['min'],
                    max_num=required_metadata[key]['max'],
                    validate_min=True,
                    validate_max=True,
                    extra=0)
                formset = formsetKlass(prefix=key, **self.get_form_kwargs())
                if(
                    key is "author" and
                    len(formset.forms) == 1 and
                    not formset.forms[0].is_bound
                ):
                    # remove any unbound author forms,
                    # even though a min is required
                    del formset.forms[0]
                for form in formset:
                    form.empty_permitted = False
                ctx["%s_formset" % key] = formset

        return ctx

    def validate_conditional_requirements(self, forms):
        """
        Uses the Class.required_metadata.conditionally_required dict
        to validate the submission
        """
        meets_reqs = True
        required_metadata = self.content_type_class.required_metadata()
        if 'conditionally_required' in required_metadata.keys():
            meets_reqs = False
            cr = required_metadata['conditionally_required']
            for formset_prefix in cr:
                if len(forms["%s_formset" % formset_prefix].forms) > 0:
                    meets_reqs = True
                    break
            if not meets_reqs:
                reqs = " or ".join(cr)
                forms['document_form'].add_error(
                    None,
                    "At least one %s is required for this resource." % reqs)
        return meets_reqs
