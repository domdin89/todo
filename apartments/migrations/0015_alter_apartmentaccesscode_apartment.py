# Generated by Django 4.0 on 2024-03-26 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0014_apartmentaccesscode_qrcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartmentaccesscode',
            name='apartment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='apartments.apartments'),
        ),
    ]
