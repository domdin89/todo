from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):  
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True, )
    
    image = models.ImageField(
        upload_to='profile_pic/', blank=True, null=True, )
    first_name = models.CharField(max_length=100, blank=True, null=True, )
    last_name = models.CharField(max_length=100, blank=True, null=True, )
    mobile_number = models.CharField(max_length=100, blank=True, null=True, )

    token = models.CharField(max_length=150, blank=True, null=True, )
    is_active = models.BooleanField(default=False )    
    email = models.CharField(max_length=100, blank=True, null=True, unique=True)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    TYPE = [
        ('USER', 'USER'),
        ('TECNICI', 'TECNICI'),
        ('STAFF', 'STAFF'),
    ]
    type = models.CharField(max_length=7, choices=TYPE, default='USER')

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.type}"
    


class Collaborators(models.Model):  
    image = models.ImageField(
        upload_to='collab_pic/', blank=True, null=True, )
    first_name = models.CharField(max_length=100, blank=True, null=True, )
    last_name = models.CharField(max_length=100, blank=True, null=True, )
    mobile_number = models.CharField(max_length=100, blank=True, null=True, )

    role = models.CharField(max_length=150, blank=True, null=True, )
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    TYPE = [
        ('PLANNER', 'PLANNER'),
        ('COLLABORATOR', 'COLLABORATOR'),
    ]
    type = models.CharField(max_length=12, choices=TYPE, default='COLLABORATOR')

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.type}"