# Generated by Django 4.0 on 2024-06-18 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_manager', '0006_file_visible_in_app'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
