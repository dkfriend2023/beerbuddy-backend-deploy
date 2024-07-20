from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import CheckboxSelectMultiple
from django.db.models import ManyToManyField
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('user_nickname', 'email', 'password')}),
        ('개인 정보', {
            'fields': (
                'user_image',
                'uni',
                'phone_number',
                'kakao_id',
                'like_restaurant',
            ),
        }),
        ('권한', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        })
    )
    readonly_fields = ['created_at']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'user_nickname',
                'email',
                'uni',
                'phone_number',
                'kakao_id',
                'like_restaurant',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    list_display = ('id', 'user_nickname', 'uni', 'email', 'is_staff')
    list_display_links = ('user_nickname',)
    search_fields = ('email', 'user_nickname')
    ordering = ('email',)

    formfield_overrides = {
        ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
