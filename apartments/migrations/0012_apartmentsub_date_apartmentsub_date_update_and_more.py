# Generated by Django 4.0 on 2024-03-04 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0011_apartmentsub_is_valid'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartmentsub',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='apartmentsub',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='checklist',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='checklist',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='checklistworksites',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='clientapartments',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='clientapartments',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='apartments',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='apartments',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='checklistworksites',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
