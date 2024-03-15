from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Profile
from django.db import transaction

class CollabAttivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(profile__is_active=True)
    
class AttivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Worksites(models.Model):
    image = models.ImageField(upload_to='worksite_images/',blank=True, null=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100,blank=True, null=True)
    lat = models.DecimalField(max_digits=10, decimal_places=6,blank=True, null=True)
    lon = models.DecimalField(max_digits=10, decimal_places=6,blank=True, null=True)
    is_visible = models.BooleanField(default=False,blank=True, null=True)
    is_active = models.BooleanField(default=True,blank=True, null=True)
    net_worth = models.FloatField(blank=True, null=True)
    percentage_worth = models.FloatField(blank=True, null=True)
    financier = models.ForeignKey('Financier', on_delete=models.CASCADE,blank=True, null=True)
    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE,blank=True, null=True)
    link = models.CharField(max_length=100,blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True,blank=True, null=True)
    codice_commessa = models.CharField(max_length=100,blank=True, null=True)
    codice_CIG = models.CharField(max_length=100,blank=True, null=True)
    codice_CUP = models.CharField(max_length=100,blank=True, null=True)
    date_start = models.DateTimeField(blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)

    CHOICES = [
        ('APERTO', 'APERTO'),
        ('SOSPESO', 'SOSPESO'),
        ('CHIUSO', 'CHIUSO'),
    ]
    status = models.CharField(max_length=20, choices=CHOICES, default='APERTO')

    objects = AttivoManager()

class WorksitesProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)

class CollabWorksites(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='collabworksites')
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE, related_name="collaborations")
    role = models.CharField(max_length=150)
    is_valid = models.BooleanField(default=True)
    date_start = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_end = models.DateTimeField(blank=True, null=True)


class CollabWorksitesOrder(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='collabworksitesOrder')
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE, related_name="collaborationsOrder")
    order = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_valid = models.BooleanField(default=True)

    objects = CollabAttivoManager()  # Il manager di default

class Categories(models.Model):
    name = models.CharField(max_length=150)

class WorksitesCategories(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE )
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE, related_name="categories")

class Status(models.Model):
    description = models.CharField(max_length=150)
    order = models.IntegerField()


class ActiveWorksiteStatusManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)
    
class WorksitesStatus(models.Model):
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="worksite_status")
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)
    active = models.BooleanField(default=True)

    objects = models.Manager()  # Il manager di default
    active_statuses = ActiveWorksiteStatusManager()  # Il nostro nuovo manager per gli stati attivi

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.active:
                # When a new active status is being saved, we deactivate all other active statuses
                # for the same worksite, but we exclude the current instance from this deactivation.
                WorksitesStatus.objects.filter(
                    worksite=self.worksite,
                    status=self.status,
                    active=True
                ).exclude(id=self.id).update(active=False)
                
            super(WorksitesStatus, self).save(*args, **kwargs)



class FoglioParticella(models.Model):
    foglio = models.CharField(max_length=50,blank=True, null=True) 
    particella = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    oggetti_attivi = AttivoManager()
    objects = models.Manager()
    
class WorksitesFoglioParticella(models.Model):
    foglio_particella = models.ForeignKey(FoglioParticella, on_delete=models.CASCADE)
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE, related_name="foglio_particelle")

class Financier(models.Model):
    name = models.CharField(max_length=150)

class Contractor(models.Model):
    name = models.CharField(max_length=150)
