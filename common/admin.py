from django.contrib import admin
from django.contrib.sites.models import Site
#from speaker.models import Category
from common.models import Theme,Option
from accounts.models import UserProfile
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1
    max_num = 1

class MyUserAdmin(UserAdmin):
    inlines = [UserProfileInline, ]

admin.site.unregister(User)
admin.site.register(Option)
admin.site.register(Theme)
admin.site.register(User, MyUserAdmin)
