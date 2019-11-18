# Django models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

# Importing my models
from players.models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'points', 'cluster', 'grade']
    list_display_links = ['pk', 'user']
    list_editable = (
        'points',
        'cluster',
        'grade'
    )

    search_fields = (
        'user__email',
        'user__username',
        'user__first_name',
        'user__last_name',
    )

    list_filter = (
        'user__is_active',
    )

class PlayerInline(admin.StackedInline):
    model = Player
    can_delete = False
    verbose_name_plural = 'Players'


class UserAdmin(BaseUserAdmin):
    inlines = (PlayerInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
