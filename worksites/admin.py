from django.contrib import admin
from .models import Worksites, CollabWorksites
# Register your models here.

class WorksitesAdmin(admin.ModelAdmin):
    #fields = ("","")
    # inlines = [ ]
    #list_display = ("id", "user", )
    # list_editable = ()
    list_per_page = 10

class CollabWorksitesAdmin(admin.ModelAdmin):
    #fields = ("","")
    # inlines = [ ]
    #list_display = ("id", "user", )
    # list_editable = ()
    list_per_page = 10

admin.site.register(Worksites, WorksitesAdmin)
admin.site.register(CollabWorksites, CollabWorksitesAdmin)