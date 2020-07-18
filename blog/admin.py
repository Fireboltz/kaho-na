from django.contrib import admin
from blog.models import Post, Like
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
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


@admin.register(Like)
class LikeAdmin(ImportExportModelAdmin, ExportActionMixin, admin.ModelAdmin):
    fieldsets = [
        ('Basic Details', {
            'fields': [
                ('post', 'user'),
                'dateTime'
            ]
        }),
    ]
    list_display = ('post', 'user', 'dateTime')
    list_filter = ('post', 'user')
