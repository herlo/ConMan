from django.contrib import admin
from django.contrib.sites.models import Site
from speakers.models import Category,Room,Status,AudienceType,Presentation

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

    class Meta:
        verbose_name_plural = "Categories"

class PresentationAdmin(admin.ModelAdmin):
    list_filter = ('status', 'cat', 'audiences')
    list_display = ('title', 'shorter_abstract', 'cat', 'status')
    search_fields = ('@longabstract','status','@title','foreign_key__cat')

    def shorter_abstract(self, obj):
        return ("%s" % (obj.short_abstract))[:400]


admin.site.register(Room)
admin.site.register(Status)
admin.site.register(AudienceType)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Presentation, PresentationAdmin)
