from django.contrib import admin
from feincms.admin.item_editor import ItemEditor
from feincms.extensions import ExtensionModelAdmin

from .models import Document


class DocumentAdmin(ItemEditor, ExtensionModelAdmin):
    pass

admin.site.register(Document, DocumentAdmin)
