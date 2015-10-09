from django.views.generic import ListView, DetailView
from .models import Document

import django_filters


class DocumentsFilter(django_filters.FilterSet):

    class Meta:
        model = Document
        fields = ('topics', 'disciplines', 'organizations')



class HomeView(ListView):
    template_name = 'home.html'

    def get_queryset(self):
        return DocumentsFilter(self.request.GET, queryset=Document.objects.all())
