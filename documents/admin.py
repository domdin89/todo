from django.contrib import admin
from .models import Documents
# Register your models here.

class DocumentsAdmin(admin.ModelAdmin):
    #fields = ("","")
    # inlines = [ ]
    #list_display = ("id", "user", )
    # list_editable = ()
    list_per_page = 10

admin.site.register(Documents, DocumentsAdmin)