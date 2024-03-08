# Generated by Django 4.0 on 2024-03-08 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('worksites', '0025_alter_worksitesstatus_date_update'),
    ]

    operations = [
        migrations.AddField(
            model_name='worksitesstatus',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='worksitesstatus',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worksite_status', to='worksites.status'),
        ),
    ]
