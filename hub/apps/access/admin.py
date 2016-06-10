from django.contrib import admin
from .models import TemporaryUser


class TemporaryUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'access_starts', 'access_ends')
admin.site.register(TemporaryUser, TemporaryUserAdmin)
