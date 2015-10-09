from __future__ import unicode_literals

from django.contrib import admin

from .models import Author, Website, Image, File, ContentType
from .types.publications import Publication
from .types.academic import AcademicProgram


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
    list_display = ('__unicode__', 'created')
    list_filter = ('created', 'modified',)
    search_fields = ('title', 'description', 'keywords',)
    inlines = (AuthorInline, WebsiteInline, FileInline, ImageInline)
    exclude = ('content_type',)
    raw_id_fields = ('organizations',)


class AllContentTypesAdmin(admin.ModelAdmin):
    list_display = ('object_link', 'content_type', 'created',)
    list_display_links = None
    actions_on_top = False
    actions_on_bottom = False

    def has_add_permission(self, request):
        return False

    def object_link(self, obj):
        return '<a href="{}">{} </a>'.format(
            getattr(obj, obj.content_type).pk,
            obj.title,
        )
    object_link.allow_tags = True
    object_link.short_description = 'Edit object'

admin.site.register(ContentType, AllContentTypesAdmin)

admin.site.register(Publication, BaseContentTypeAdmin)
admin.site.register(AcademicProgram, BaseContentTypeAdmin)
