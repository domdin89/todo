from django.db import models
from accounts.models import Profile
from worksites.models import Worksites
from apartments.models import Apartments


class Survey(models.Model):
    name = models.CharField(max_length=250)

class BoardRead(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    board = models.ForeignKey('Boards', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

class BoardAttachments(models.Model):
    board = models.ForeignKey('Boards', on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, blank=True, null=True)
    attachment_link = models.CharField(max_length=200, blank=True, null=True)
    TYPE_CHOICES = [
        ('DOCUMENT', 'DOCUMENT'),
        ('IMAGE', 'IMAGE'),
    ]
    type = models.CharField(max_length=8, choices=TYPE_CHOICES, default='IMAGE')
    date = models.DateTimeField(auto_now_add=True)

class Boards(models.Model):
    worksite = models.ForeignKey(Worksites, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='board_images/')
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    recipients = models.IntegerField(blank=True, null=True)
    TYPE_CHOICES = [
        ('MESSAGE', 'MESSAGE'),
        ('UPDATE', 'UPDATE'),
    ]
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='MESSAGE')