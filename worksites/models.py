from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile


class Worksites(models.Model):
    image = models.ImageField(upload_to='worksite_images/')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    lat = models.DecimalField(max_digits=10, decimal_places=6)
    lon = models.DecimalField(max_digits=10, decimal_places=6)
    is_open = models.BooleanField(default=False)
    net_worth = models.FloatField()
    financier = models.ForeignKey('Financier', on_delete=models.CASCADE)
    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE)
    link = models.CharField(max_length=100,blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    TYPE_CHOICES = [
        ('ABITAZIONE', 'ABITAZIONE'),
        ('GARAGE', 'GARAGE'),
        ('LOCALE COMMERCIALE', 'LOCALE COMMERCIALE'),
        ('TERRENO', 'TERRENO'),
    ]
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='ABITAZIONE')

class WorksitesProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)


class CollabWorksites(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)
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
