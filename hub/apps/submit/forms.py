from django import forms


from ..content.models import Author

class SubmitResourceForm(forms.ModelForm):
    """
    A very generic ModelForm that is later executed by a modelform_factory.
    We'll just add some very generic validation here.
    """
    class Meta:
        exclude = (
            'id',
            'content_type',
            'status',
            'member_only',
            'featured',
            'published',
            'organizations'
        )

    def save(self, request):
        return super(SubmitResourceForm, self).save()

    def clean_affirmation(self):
        if not self.cleaned_data.get('affirmation'):
            raise forms.ValidationError('You need to acknowledge the affirmation')
        return self.cleaned_data.get('affirmation')


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ('id', 'ct', 'organization')
