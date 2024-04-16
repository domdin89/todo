from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


from accounts.models import Profile

@receiver(pre_save, sender=User)
def check_user_email(sender, instance, **kwargs):
    # Controllo se l'email è già utilizzata escludendo l'istanza attuale se sta venendo aggiornata
    if User.objects.filter(email=instance.email).exclude(pk=instance.pk).exists():
        raise ValidationError(f"The email address {instance.email} is already in use.")