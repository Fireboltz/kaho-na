from django.contrib import admin
from blog.models import Post
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(Post)
class NewsAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                ('title', 'date'),
                ('author', 'pinned', 'draft'),
                'description'
            ]
        }),
    ]
    list_display = ('title', 'date', 'pinned')
    list_filter = ('pinned', 'draft')
