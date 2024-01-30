from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import Collaborators
from accounts.models import Profile


class Worksites(models.Model):  
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True, )

    image = models.ImageField(
        upload_to='worksite_pic/', blank=True, null=True, )
    name = models.CharField(max_length=100, blank=True, null=True, )
    address = models.CharField(max_length=100, blank=True, null=True, )
    city = models.CharField(max_length=100, blank=True, null=True, )
    region = models.CharField(max_length=100, blank=True, null=True, )
    is_open = models.BooleanField(default=True)

    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name
    

class CollabWorksites(models.Model):  
    collaborator = models.ForeignKey(
        Collaborators, on_delete=models.CASCADE, blank=True, null=True, )
    worksite = models.ForeignKey(
        Worksites, on_delete=models.CASCADE, blank=True, null=True, )
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.profile.first_name} {self.apartment}"