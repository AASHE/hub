from django.contrib import admin
from . import models


class SustainabilityTopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(models.SustainabilityTopic, SustainabilityTopicAdmin)
admin.site.register(models.AcademicDiscipline)
admin.site.register(models.InstitutionalOffice)
admin.site.register(models.ProgramType)
admin.site.register(models.Country)
