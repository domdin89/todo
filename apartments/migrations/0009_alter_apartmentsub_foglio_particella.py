# Generated by Django 4.0 on 2024-02-24 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksites', '0013_alter_worksites_codice_cig_and_more'),
        ('apartments', '0008_alter_apartmentsub_sub'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentsub',
            name='foglio_particella',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='worksites.foglioparticella'),
        ),
    ]
