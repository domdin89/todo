# Generated by Django 4.0 on 2024-04-15 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_email_visible_profile_img_visible_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_visible',
            field=models.BooleanField(default=False),
        ),
    ]
