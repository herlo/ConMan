from django.contrib import admin
from django.contrib.sites.models import Site
from lugs.models import LUG, Type

import Image

site = admin.AdminSite()

admin.site.register(Type)

class LUGAdmin(admin.ModelAdmin):
	#fields = ['company','contact','level']
	list_display = ('name','contact','type')

admin.site.register(LUG, LUGAdmin)
