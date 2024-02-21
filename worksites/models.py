from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile


class Worksites(models.Model):
    image = models.ImageField(upload_to='worksite_images/',blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6,blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=6,blank=True, null=True)
    is_visible = models.BooleanField(default=False,blank=True, null=True)
    net_worth = models.FloatField(blank=True, null=True)
    percentage_worth = models.FloatField(blank=True, null=True)
    financier = models.ForeignKey('Financier', on_delete=models.CASCADE,blank=True, null=True)
    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE,blank=True, null=True)
    link = models.CharField(max_length=100,blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True,blank=True, null=True)
    codice_commessa = models.CharField(max_length=100,blank=True, null=True, unique=True)
    codice_CIG = models.CharField(max_length=100,blank=True, null=True, unique=True)
    codice_CUP = models.CharField(max_length=100,blank=True, null=True, unique=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)

    CHOICES = [
        ('APERTO', 'MESSAGE'),
        ('SOSPESO', 'UPDATE'),
        ('CHIUSA', 'UPDATE'),
    ]
    status = models.CharField(max_length=20, choices=CHOICES, default='APERTO')

class WorksitesProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)

class CollabWorksites(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name='collabworksites')
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE, related_name="collaborations")
    role = models.CharField(max_length=150)
    order = models.IntegerField()
    date_start = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)

class Categories(models.Model):
    name = models.CharField(max_length=150)

class WorksitesCategories(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE )
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE, related_name="categories")

class FoglioParticella(models.Model):
    foglio = models.CharField(max_length=50,blank=True, null=True) 
    particella = models.CharField(max_length=50, blank=True, null=True)
    
class WorksitesFoglioParticella(models.Model):
    foglio_particella = models.ForeignKey(FoglioParticella, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE, related_name="foglio_particelle")

class Financier(models.Model):
    name = models.CharField(max_length=150)

class Contractor(models.Model):
    name = models.CharField(max_length=150)
