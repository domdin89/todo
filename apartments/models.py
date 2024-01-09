from accounts.models import Profile
from django.db import models
from django.utils.translation import gettext_lazy as _
from worksites.models import Worksites
from django.core.exceptions import ValidationError


class Apartments(models.Model):  
    worksite = models.ForeignKey(
        Worksites, on_delete=models.CASCADE, blank=True, null=True, )
    name = models.CharField(max_length=250, blank=True, null=True, )
    surface = models.CharField(max_length=100, blank=True, null=True, )
    note = models.CharField(max_length=100, blank=True, null=True, )
    owner = models.CharField(max_length=100, blank=True, null=True, )
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.worksite.name} {self.surface}"


class UserApartments(models.Model):  
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True, )
    apartment = models.ForeignKey(
        Apartments, on_delete=models.CASCADE, blank=True, null=True, )
    worksite = models.ForeignKey(
        Worksites, on_delete=models.CASCADE, blank=True, null=True, )
    

    def clean(self):
        # Controlla che almeno uno dei due campi non sia nullo
        if not (self.profile or self.worksite):
            raise ValidationError("Deve essere impostato almeno uno tra profilo o appartamento.")

    def save(self, *args, **kwargs):
        self.clean()
        super(UserApartments, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.profile.first_name} {self.apartment}"