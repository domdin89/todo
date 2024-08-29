from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    checked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.name} - checked: {self.checked} - is_deleted: {self.is_deleted}'