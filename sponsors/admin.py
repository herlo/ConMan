from django.contrib import admin
from django.contrib.sites.models import Site
from sponsors.models import Sponsor,Level

site = admin.AdminSite()


admin.site.register(Level)
admin.site.register(Sponsor)
