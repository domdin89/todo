# Generated by Django 4.0 on 2024-02-01 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksites', '0003_alter_worksites_contractor_alter_worksites_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collabworksites',
            name='worksite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collaborations', to='worksites.worksites'),
        ),
    ]
