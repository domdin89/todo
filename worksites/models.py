from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile


class Worksites(models.Model):
    image = models.ImageField(upload_to='worksite_images/',blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6,blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=6,blank=True, null=True)
    is_open = models.BooleanField(default=False,blank=True, null=True)
    net_worth = models.FloatField(blank=True, null=True)
    financier = models.ForeignKey('Financier', on_delete=models.CASCADE,blank=True, null=True)
    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE,blank=True, null=True)
    link = models.CharField(max_length=100,blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True,blank=True, null=True)

class WorksitesProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)

class CollabWorksites(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE, related_name="collaborations")
    role = models.CharField(max_length=150)
    order = models.IntegerField()


class Categories(models.Model):
    name = models.CharField(max_length=150)

class WorksitesCategories(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)



class CheckList(models.Model):
    name = models.CharField(max_length=100)

class CheckListWorksites(models.Model):
    worksites = models.ForeignKey(Worksites, on_delete=models.CASCADE)
    checklist = models.ForeignKey(CheckList, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField()
    is_done = models.BooleanField(default=False)



class Financier(models.Model):
    name = models.CharField(max_length=150)

class Contractor(models.Model):
    name = models.CharField(max_length=150)
