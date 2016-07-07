from django.contrib import admin
from . import models


class SustainabilityTopicFavoriteAdmin(admin.TabularInline):
    model = models.SustainabilityTopicFavorite
    raw_id_fields = ('ct',)
    list_display = ('order',)
    list_editable = ('order',)
    extra = 0


class SustainabilityTopicAdmin(admin.ModelAdmin):
    inlines = (SustainabilityTopicFavoriteAdmin,)
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'order')
    list_editable = ('order',)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'country')
    search_fields = ('org_name', 'country', 'state')
    actions = None

    def get_readonly_fields(self, request, obj=None):
        """Treat all fields as read-only"""
        return [i.name for i in obj._meta.fields]

    def has_add_permission(self, request):
        """Nobody is allowed to add records."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Nobody is allowed to add records."""
        return False

admin.site.register(models.SustainabilityTopic, SustainabilityTopicAdmin)
admin.site.register(models.AcademicDiscipline)
admin.site.register(models.InstitutionalOffice)
admin.site.register(models.ProgramType)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.ConferenceName)
admin.site.register(models.PresentationType)
