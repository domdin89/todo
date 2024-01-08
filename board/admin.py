from django.contrib import admin
from .models import Boards
# Register your models here.

class BoardsAdmin(admin.ModelAdmin):
    #fields = ("","")
    # inlines = [ ]
    #list_display = ("id", "user", )
    # list_editable = ()
    list_per_page = 10

admin.site.register(Boards, BoardsAdmin)