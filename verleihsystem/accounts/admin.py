from django.contrib import admin
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class UserProfileInline(admin.StackedInline):
    """
    Inline for editing the profile on the user admin page.
    """
    model = UserProfile
    max_num = 1
    can_delete = False


class FullUserAdmin(UserAdmin):
    """
    Admin for a user with a profile inline.
    """
    inlines = [UserProfileInline]


# Unregister the Django default user admin
admin.site.unregister(User)
admin.site.register(User, FullUserAdmin)
