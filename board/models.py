from django.db import models
from accounts.models import Profile
from worksites.models import Worksites
from apartments.models import Apartments


class Survey(models.Model):
    name = models.CharField(max_length=250)

class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

class SurveyQuestionChoices(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
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

class BoardsRecipient(models.Model):
    board = models.ForeignKey('Boards', on_delete=models.CASCADE, related_name="recipients")
    TYPE_CHOICES = [
        ('APARTMENT', 'APARTMENT'),
        ('WORKSITE', 'WORKSITE'),
        ('PROFILE', 'PROFILE'),
    ]
    recipient_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='WORKSITE')
    date = models.DateTimeField(auto_now_add=True)
    worksites = models.ForeignKey(Worksites, on_delete=models.CASCADE, blank=True, null=True)
    apartment = models.ForeignKey(Apartments, on_delete=models.CASCADE, blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)

class Boards(models.Model):
    image = models.ImageField(upload_to='board_images/', blank=True, null=True)
    title = models.CharField(max_length=250)
    body = models.TextField()
    author = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    TYPE_CHOICES = [
        ('MESSAGE', 'MESSAGE'),
        ('UPDATE', 'UPDATE'),
    ]
    type = models.CharField(max_length=7, choices=TYPE_CHOICES, default='MESSAGE')