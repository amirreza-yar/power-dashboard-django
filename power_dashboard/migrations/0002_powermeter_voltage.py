# Generated by Django 4.2.7 on 2023-12-23 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('power_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='powermeter',
            name='voltage',
            field=models.FloatField(default=0),
        ),
    ]