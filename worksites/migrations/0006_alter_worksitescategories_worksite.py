# Generated by Django 4.0 on 2024-02-02 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksites', '0005_remove_worksites_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksitescategories',
            name='worksite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='worksites.worksites'),
        ),
    ]
