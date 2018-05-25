from django import forms

from ..browse.forms import LeanSelectMultiple, LeanSelect
from ..content.models import Author, File, Image, Website
from . import utils


class SubmitResourceForm(forms.ModelForm):
    """
    A very generic ModelForm that is later executed by a modelform_factory.
    We'll just add some very generic validation here.
    """

    class Meta:
        widgets = {
            'topics': forms.widgets.SelectMultiple,
            'disciplines': forms.widgets.SelectMultiple,
            'organizations': LeanSelectMultiple,
        }

        exclude = (
            'id',
            'content_type',
            'status',
            'permission',
            'submitted_by',
            'published',
            'notes',
            'slug',
        )

    def clean_topics(self):
        selected_topics = self.cleaned_data.get('topics')
        required_topics = self.instance.preset_topics()
        for required_topic in required_topics:
            if required_topic not in selected_topics:
                msg = "The following topics are required: %s" % (
                    ", ".join([x.name for x in required_topics]))
                raise forms.ValidationError(msg)

        if selected_topics and len(selected_topics) > 3:
            raise forms.ValidationError('Please choose no more than 3 topics.')
        return selected_topics

    def clean_disciplines(self):
        disciplines = self.cleaned_data.get('disciplines')
        if disciplines and len(disciplines) > 3:
            raise forms.ValidationError(
                'Please choose no more than 3 disciplines.')
        return disciplines

    def clean_institutions(self):
        institutions = self.cleaned_data.get('institutions')
        if institutions and len(institutions) > 3:
            raise forms.ValidationError(
                'Please choose no more than 3 institutions.')
        return institutions

    def save(self, request):

        self.instance.submitted_by = request.user
        obj = super(SubmitResourceForm, self).save()

        # Add the requst.User as an author
        if self.cleaned_data.get('user_is_author'):
            Author.objects.create(ct=obj, email=request.user.email,
                                  name=request.user.get_full_name())

        utils.send_resource_submitted_email(resource=self.instance,
                                            submitter=self.instance.submitted_by,
                                            request=request)
        return obj


class AffirmationMixin(object):

    def clean_affirmation(self):
        if not self.cleaned_data.get('affirmation'):
            raise forms.ValidationError(
                'You need to acknowledge the affirmation')
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


class FileForm(AffirmationMixin, forms.ModelForm):
    class Meta:
        model = File
        exclude = ('id', 'ct')

    def __init__(self, *args, **kwargs):
        super(FileForm, self).__init__(*args, **kwargs)
        self.fields['item'].required = True
        self.fields['affirmation'].required = True

    def save(self, instance):
        self.instance.ct = instance
        return super(FileForm, self).save()


class ImageForm(AffirmationMixin, forms.ModelForm):
    class Meta:
        model = Image
        exclude = ('id', 'ct', 'small_thumbnail', 'med_thumbnail')

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].required = True
        self.fields['affirmation'].required = True

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
