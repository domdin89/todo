# Generated by Django 3.2 on 2022-12-07 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_cantina_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cantina',
            name='user',
        ),
    ]
