# Generated by Django 4.0 on 2024-04-15 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0005_directory_apartment'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='visible_in_app',
            field=models.BooleanField(default=False),
        ),
    ]
