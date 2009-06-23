from django.contrib import admin
from volunteers.models import Volunteer, VolunteerRole


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['volunteer', 'requested', 'role']
    list_filter = ['role','requested']
    search_fields = ['@comments']


class VolunteerRoleAdmin(admin.ModelAdmin):
    pass


vol_admin = admin.AdminSite()
for adm in [vol_admin, admin.site]:
    adm.register(Volunteer, VolunteerAdmin)
    adm.register(VolunteerRole, VolunteerRoleAdmin)
