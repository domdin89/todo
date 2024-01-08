from django.contrib import admin
from .models import Profile
# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    #fields = ("","")
    # inlines = [ ]
    list_display = ("id", "user", )
    # list_editable = ()
    list_per_page = 10

admin.site.register(Profile, ProfileAdmin)