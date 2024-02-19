from accounts.models import Profile
from django.db import models
from django.utils.translation import gettext_lazy as _
from worksites.models import FoglioParticella, Worksites
from django.core.exceptions import ValidationError

class Apartments(models.Model):
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)
    floor = models.CharField(max_length=100, blank=True, null=True)
    note = models.CharField(max_length=100, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    owner_phone = models.CharField(max_length=100,blank=True, null=True)
    owner_email = models.EmailField(blank=True, null=True)
    owner_cf = models.CharField(max_length=100, blank=True, null=True)
    link = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

class ApartmentSub(models.Model):
    sub = models.IntegerField(blank=True, null=True)
    foglio_particella = models.ForeignKey(FoglioParticella, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE, related_name='subs')

class ClientApartments(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

class CheckList(models.Model):
    name = models.CharField(max_length=100)

class CheckListWorksites(models.Model):
    worksites = models.ForeignKey(Worksites, on_delete=models.CASCADE)
    checklist = models.ForeignKey(CheckList, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField()
    is_done = models.BooleanField(default=False)