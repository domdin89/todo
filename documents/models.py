from django.db import models
from django.utils.translation import gettext_lazy as _
from board.models import Boards



class Documents(models.Model):  
    board = models.ForeignKey(
        Boards, on_delete=models.CASCADE, blank=True, null=True)

    file = models.FileField(
        upload_to='documents/', blank=True, null=True)

    def __str__(self):
        return f"{self.board}"