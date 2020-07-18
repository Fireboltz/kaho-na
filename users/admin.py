from django.contrib import admin
from users.models import Profile
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(Profile)
class ProfileAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                'user',
                ('phone', 'private'),
                'bio'
            ]
        }),
    ]
    list_display = ('user', 'private')
    list_filter = ('user', 'private')
