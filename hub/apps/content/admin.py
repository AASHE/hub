from __future__ import unicode_literals

from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import Author, Website, Image, File, ContentType, CONTENT_TYPES


class AuthorInline(admin.TabularInline):
    model = Author
    extra = 0
    raw_id_fields = ('organization',)


class WebsiteInline(admin.TabularInline):
    model = Website
    extra = 0


class FileInline(admin.TabularInline):
    model = File
    extra = 0


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0


class BaseContentTypeAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'member_only', 'published')
    list_filter = ('status', 'member_only', 'created', 'published',)
    search_fields = ('title', 'description', 'keywords',)
    inlines = (AuthorInline, WebsiteInline, FileInline, ImageInline)
    exclude = ('content_type',)
    raw_id_fields = ('organizations',)


class AllContentTypesAdmin(admin.ModelAdmin):
    list_display = ('status', 'object_link', 'content_type_name', 'created', 'published',)
    list_display_links = None
    actions_on_top = False
    actions_on_bottom = False

    def has_add_permission(self, request):
        return False

    def object_link(self, obj):
        ct_name = CONTENT_TYPES[obj.content_type]._meta.model_name.lower()
        return '<a href="{}">{} </a>'.format(
            reverse('admin:content_{}_change'.format(ct_name),
                    args=[getattr(obj, ct_name).pk]), obj.title)
    object_link.allow_tags = True
    object_link.short_description = 'Edit object'

    def content_type_name(self, obj):
        return CONTENT_TYPES[obj.content_type]._meta.verbose_name
    content_type_name.short_description = 'Content Type'

admin.site.register(ContentType, AllContentTypesAdmin)

for _, model in CONTENT_TYPES.items():
    admin.site.register(model, BaseContentTypeAdmin)
