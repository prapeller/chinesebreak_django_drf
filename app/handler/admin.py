from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from elements.models import Word, Grammar, Character
from structure.models import Lang, Course, Topic, Lesson, Task


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'username', 'is_active', 'is_staff', 'is_superuser']
    fieldsets = (
        (_('Credentials'), {'fields': ('email', 'username')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (_('Credentials'), {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

# users
admin.site.register(get_user_model(), UserAdmin)

# elements
admin.site.register(Word)
admin.site.register(Grammar)
admin.site.register(Character)

# structure
admin.site.register(Lang)
admin.site.register(Course)
admin.site.register(Topic)
admin.site.register(Lesson)
admin.site.register(Task)

