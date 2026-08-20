from django.contrib import admin
from apps.user.models import User
from django.utils.safestring import mark_safe


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'get_avatar',
        'first_name',
        'last_name',
        'position',
        'is_active',
        'is_staff',
        'date_joined',
        'show_is_deleted'
    )

    @admin.display(description='Avatar')
    def get_avatar(self, obj):
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" style="max-height: 40px; border-radius: 50%;" />')
        return '-No photo-'

    @admin.display(boolean=True, description='IS DELETED?')
    def show_is_deleted(self, obj):
        return obj.is_deleted

