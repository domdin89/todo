from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField



class AttivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    

class Profile(models.Model):  
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True, )
    
    image = models.ImageField(
        upload_to='profile_pic/', blank=True, null=True, )
    first_name = models.CharField(max_length=100, blank=True, null=True, )
    last_name = models.CharField(max_length=100, blank=True, null=True, )
    mobile_number = models.CharField(max_length=100, blank=True, null=True, )

    token = models.CharField(max_length=150, blank=True, null=True, )
    is_active = models.BooleanField(default=True )    
    need_change_password = models.BooleanField(default=False )
    email = models.CharField(max_length=100, blank=True, null=True)
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
    
    objects = AttivoManager()


class Privacy(models.Model):
    testo=RichTextField(blank=True, null=True) 
    data_da = models.DateField(auto_now_add=False)
    data_a = models.DateField(auto_now_add=False, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'{self.testo}'

class PrivacyAcceptance(models.Model):
    privacy = models.ForeignKey(
        Privacy, on_delete=models.CASCADE, blank=True, null=True, )
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, blank=True, null=True, )
    date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True)


    def __str__(self):
        return f'{self.privacy}'