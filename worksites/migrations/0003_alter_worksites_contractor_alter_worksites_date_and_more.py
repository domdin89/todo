# Generated by Django 4.0 on 2024-02-01 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksites', '0002_alter_worksites_address_alter_worksites_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksites',
            name='contractor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='worksites.contractor'),
        ),
        migrations.AlterField(
            model_name='worksites',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='worksites',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='worksites',
            name='financier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='worksites.financier'),
        ),
        migrations.AlterField(
            model_name='worksites',
            name='is_open',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
