from django.contrib import admin
from .models import Firebase, LastVersion
# Register your models here.


@admin.register(Firebase)
class FirebaseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Firebase._meta.fields]

@admin.register(LastVersion)
class LastVersionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LastVersion._meta.fields]