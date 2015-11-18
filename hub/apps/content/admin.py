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
    list_display = ('__unicode__', 'permission', 'published')
    list_filter = ('status', 'permission', 'created', 'published',)
    search_fields = ('title', 'description', 'keywords',)
    readonly_fields = ('published',)
    inlines = (AuthorInline, WebsiteInline, FileInline, ImageInline)
    exclude = ('content_type',)
    raw_id_fields = ('organizations', 'submitted_by')

    def _update_application_index(self):
        # from django.core import management
        # management.call_command('update_index', '{}.{}'.format(
        #     self.model._meta.app_label,
        #     self.model._meta.model_name
        # ))
        pass

    def response_add(self, request, obj):
        self._update_application_index()
        return super(BaseContentTypeAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        self._update_application_index()
        return super(BaseContentTypeAdmin, self).response_change(request, obj)

    def response_delete(self, request, obj_display, obj_id):
        self._update_application_index()
        return super(BaseContentTypeAdmin, self).response_delete(request, obj_display, obj_id)


class AllContentTypesAdmin(admin.ModelAdmin):
    list_display = ('select_link', 'status', 'object_link', 'content_type_name', 'created', 'published',)
    list_filter = ('status', 'topics', 'permission', 'created', 'published',)
    list_display_links = ('select_link',)
    actions_on_top = False
    actions_on_bottom = False

    def has_add_permission(self, request):
        return False

    def select_link(self, obj):
        return 'Favorite'
    select_link.allow_tags = True
    select_link.short_description = ''

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
