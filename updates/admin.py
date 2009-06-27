from django.contrib import admin
from django.contrib.sites.models import Site
from updates.models import Update


class UpdateAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated', 'author')
    

admin.site.register(Update, UpdateAdmin)
