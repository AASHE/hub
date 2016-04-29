from __future__ import unicode_literals

from django.contrib import admin
from django.core.urlresolvers import reverse

from . import utils
from .models import Author, Website, Image, File, ContentType, CONTENT_TYPES
from .types.casestudies import CaseStudy
from .types.publications import Publication
from django.utils import timezone
from model_utils import Choices


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


# Custom model form for the admin
from django import forms
from ..browse.forms import LeanSelectMultiple
class ContentTypeAdminForm(forms.ModelForm):
    class Meta:
        model = ContentType
        fields = '__all__'
        widgets = {
            'organizations': LeanSelectMultiple(),
            # 'keywords': LeanSelectMultiple(),
            # 'keywords': forms.SelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ContentTypeAdminForm, self).__init__(*args, **kwargs)
        # import pdb; pdb.set_trace()
        # tag_choices = ContentType.keywords.tag_model.objects.distinct('name').order_by('name')
        # tag_choices = tag_choices.values_list('pk', 'name')
        # self.fields['keywords'].widget.choices = tag_choices


class BaseContentTypeAdmin(admin.ModelAdmin):
    form = ContentTypeAdminForm
    
    def save_model(self, request, obj, form, change):
        status_tracker_changed = obj.status_tracker.changed()  # before save
        obj.save()
        if status_tracker_changed:
            if obj.status == obj.STATUS_CHOICES.published:
                utils.send_resource_approved_email(obj, request)
            elif obj.status == obj.STATUS_CHOICES.declined:
                utils.send_resource_declined_email(obj, request)


class SpecificContentTypeAdmin(BaseContentTypeAdmin):
    list_display = ('__unicode__', 'permission', 'published',)
    list_filter = ('status', 'permission', 'created', 'published',)
    search_fields = ('title', 'description', 'keywords',)
    readonly_fields = ('published',)
    inlines = (AuthorInline, WebsiteInline, FileInline, ImageInline)
    exclude = ('content_type',)
    raw_id_fields = ('submitted_by',)

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
        return super(BaseContentTypeAdmin, self).response_delete(request,
                                                                 obj_display,
                                                                 obj_id)


class AllContentTypesAdmin(BaseContentTypeAdmin):
    list_display = ('select_link', 'status', 'object_link',
                    'content_type_name', 'created', 'published', 'notes')
    list_filter = ('status', 'topics', 'permission', 'created', 'published',)
    list_sort = ('object_link', 'content_type_name',)
    list_display_links = ('select_link',)
    actions_on_top = True
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
    object_link.admin_order_field = 'slug'

    def content_type_name(self, obj):
        return CONTENT_TYPES[obj.content_type]._meta.verbose_name
    content_type_name.short_description = 'Content Type'
    content_type_name.admin_order_field = 'content_type'

    STATUS_CHOICES = Choices(
        ('new', 'New'),
        ('published', 'Published'),
        ('declined', 'Declined')
    )

    def change_status(self, request, queryset, new_status):
        # changes the status of selected content to `new_status`
        for obj in queryset:
            # Need to retrieve the child instance first
            child_class = CONTENT_TYPES[obj.content_type]
            obj = child_class.objects.get(pk=obj.pk)
            obj.status = new_status
            self.save_model(self, obj=obj, form=None, change=None)
        if len(queryset) == 1:
            message_bit = "1 item was"
        else:
            message_bit = "%s items were" % len(queryset)
        self.message_user(
            request, "%s changed to status: %s" % (message_bit, new_status))

    def publish(self, request, queryset):
        # Changes status of selected content to "Published"
        self.change_status(request, queryset, self.STATUS_CHOICES.published)
    publish.short_description = 'Publish selected content'

    def unpublish(self, request, queryset):
        # Resets status of content to "New"
        self.change_status(request, queryset, self.STATUS_CHOICES.new)
    unpublish.short_description = 'Unpublish selected content'

    def decline(self, request, queryset):
        # Changes status of selected content to "Declined"
        self.change_status(request, queryset, self.STATUS_CHOICES.declined)
    decline.short_description = 'Decline selected content'

    actions = [publish, unpublish, decline]

admin.site.register(ContentType, AllContentTypesAdmin)

# register each content type
# case studies and publications require custom admins

for _, model in CONTENT_TYPES.items():
    if _ != 'publication' and _ != 'casestudy':
        admin.site.register(model, SpecificContentTypeAdmin)


class PublicationAdmin(SpecificContentTypeAdmin):
    list_display = ('__unicode__', 'permission', 'published', 'release_date', '_type')
    list_filter = ('status', 'permission', 'created', 'published', 'release_date', '_type')
    
admin.site.register(Publication, PublicationAdmin)


class CaseStudyAdmin(SpecificContentTypeAdmin):
    list_display = ('__unicode__', 'permission', 'published', 'consider_for_award')
    list_filter = ('status', 'permission', 'created', 'published', 'consider_for_award')
    
admin.site.register(CaseStudy, CaseStudyAdmin)
