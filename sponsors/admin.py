from django.contrib import admin
from django.contrib.sites.models import Site
from sponsors.models import Sponsor,Level

site = admin.AdminSite()

admin.site.register(Level)


class SponsorAdmin(admin.ModelAdmin):
	#fields = ['company','contact','level']
	list_display = ('company','contact','level')

admin.site.register(Sponsor, SponsorAdmin)
