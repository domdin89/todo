from django.db import models

# Create your models here.
class Firebase(models.Model):
    token = models.CharField(max_length=500, blank=True, null=True, unique=True)
    uid = models.CharField(max_length=255, blank=True, null=True, unique=True)
    additional_params = models.TextField(blank=True, null=True)
    permissions = models.JSONField(default=dict)

    consent = models.BooleanField(default=False)
    last_access = models.DateTimeField(auto_now_add=True,  blank=True, null=True,)
    count = models.IntegerField(default=0)
    userId = models.CharField(max_length=500, blank=True, null=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    platform = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.token

class LastVersion(models.Model):
    platform = models.CharField(max_length=50, blank=True, null=True,unique=True)
    version = models.CharField(max_length=50, blank=True, null=True)
    required = models.BooleanField(default=False)

    def __str__(self):
        return self.platform