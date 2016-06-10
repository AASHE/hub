from django.contrib import admin
from .models import TemporaryUser


class TemporaryUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(TemporaryUser, TemporaryUserAdmin)
