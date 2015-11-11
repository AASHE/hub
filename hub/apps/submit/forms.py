from django import forms

from ..browse.filter import LeanSelectMultiple, LeanSelect
from ..content.models import Author, File, Image, Website

class SubmitResourceForm(forms.ModelForm):
    """
    A very generic ModelForm that is later executed by a modelform_factory.
    We'll just add some very generic validation here.
    """
    class Meta:
        widgets = {
            'topics': forms.widgets.CheckboxSelectMultiple,
            'disciplines': forms.widgets.CheckboxSelectMultiple,
            'organizations': LeanSelectMultiple,
        }
        exclude = (
            'id',
            'content_type',
            'status',
            'permission',
            'submitted_by',
            'published',
        )

    def save(self, request):
        if request.user.is_authenticated():
            self.instance.submitted_by = request.user
        return super(SubmitResourceForm, self).save()

    def clean_affirmation(self):
        if not self.cleaned_data.get('affirmation'):
            raise forms.ValidationError('You need to acknowledge the affirmation')
        return self.cleaned_data.get('affirmation')


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ('id', 'ct')
        widgets = {
            'organization': LeanSelect,
        }

    def save(self, instance):
        self.instance.ct = instance
        return super(AuthorForm, self).save()


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ('id', 'ct')

    def save(self, instance):
        self.instance.ct = instance
        return super(FileForm, self).save()


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('id', 'ct')

    def save(self, instance):
        self.instance.ct = instance
        return super(ImageForm, self).save()


class WebsiteForm(forms.ModelForm):
    class Meta:
        model = Website
        exclude = ('id', 'ct')

    def save(self, instance):
        self.instance.ct = instance
        return super(WebsiteForm, self).save()
