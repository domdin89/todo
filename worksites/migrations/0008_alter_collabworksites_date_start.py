# Generated by Django 4.0 on 2024-02-12 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('worksites', '0007_remove_checklistworksites_checklist_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collabworksites',
            name='date_start',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
