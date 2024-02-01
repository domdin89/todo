from accounts.models import Profile
from django.db import models
from django.utils.translation import gettext_lazy as _
from worksites.models import Worksites
from django.core.exceptions import ValidationError

class Apartments(models.Model):
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)
    foglio = models.IntegerField(blank=True, null=True)
    particella = models.IntegerField(blank=True, null=True)
    sub = models.IntegerField(blank=True, null=True)
    surface = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    owner_phone = models.CharField(max_length=100,blank=True, null=True)
    owner_email = models.EmailField(blank=True, null=True)
    owner_cf = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)


class ClientApartments(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)