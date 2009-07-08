from django.contrib import admin
from django.contrib.sites.models import Site
#from speaker.models import Category
from common.models import ShirtSize, UserProfile
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    extra = 1
    max_num = 1

#class UserProfileAdmin(admin.ModelAdmin):
#    search_fields = ['job_title','common_channels','@bio','site']
#    list_display = ('user', 'irc_nick', 'common_channels')

class MyUserAdmin(UserAdmin):
    inlines = [UserProfileInline, ]

class ShirtSizeAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ('name', 'id')


admin.site.unregister(User)
#admin.site.unregister(ShirtSize)
admin.site.register(ShirtSize, ShirtSizeAdmin)
admin.site.register(User, MyUserAdmin)
