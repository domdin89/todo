from django.contrib import admin
from .models import Apartments, UserApartments
# Register your models here.

class ApartmentsAdmin(admin.ModelAdmin):
    #fields = ("","")
    # inlines = [ ]
    #list_display = ("id", "user", )
    # list_editable = ()
    list_per_page = 10

class UserApartmentsAdmin(admin.ModelAdmin):
    #fields = ("","")
    # inlines = [ ]
    #list_display = ("id", "user", )
    # list_editable = ()
    list_per_page = 10

admin.site.register(Apartments, ApartmentsAdmin)
admin.site.register(UserApartments, UserApartmentsAdmin)