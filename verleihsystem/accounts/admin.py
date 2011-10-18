from django.contrib import admin
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    max_num = 1
    can_delete = False


class FullUserAdmin(UserAdmin):
 inlines = [UserProfileInline]


admin.site.unregister(User)
admin.site.register(User, FullUserAdmin)
