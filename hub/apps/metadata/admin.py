from django.contrib import admin
from . import models


class SustainabilityTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class OrganizationAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        """Treat all fields as read-only"""
        return [i.name for i in obj._meta.fields]

    def has_add_permission(self, request):
        """Nobody is allowed to add records."""
        return False

    def has_delete_permission(self, request, obj):
        """Nobody is allowed to add records."""
        return False

admin.site.register(models.SustainabilityTopic, SustainabilityTopicAdmin)
admin.site.register(models.AcademicDiscipline)
admin.site.register(models.InstitutionalOffice)
admin.site.register(models.ProgramType)
admin.site.register(models.Country)
admin.site.register(models.Organization, OrganizationAdmin)
