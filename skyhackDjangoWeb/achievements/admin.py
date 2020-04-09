# Django modules
from django.contrib import admin

# My modules
from achievements.models import Achievement

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'points', 'description', 'type']

    list_display_links = ['pk', 'title']

    list_editable = (
        'points',
        'description'
    )

    search_fields = (
        'title',
        'points',
        'type'
    )

    list_filter = (
        'type',
        'points'
    )
