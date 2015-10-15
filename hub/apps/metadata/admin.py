from django.contrib import admin
from . import models


class SustainabilityTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class OrganizationAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

admin.site.register(models.SustainabilityTopic, SustainabilityTopicAdmin)
admin.site.register(models.AcademicDiscipline)
admin.site.register(models.InstitutionalOffice)
admin.site.register(models.ProgramType)
admin.site.register(models.Country)
admin.site.register(models.Organization, OrganizationAdmin)
