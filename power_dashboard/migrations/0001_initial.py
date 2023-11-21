# Generated by Django 4.2.7 on 2023-11-21 09:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PowerMeter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.FloatField()),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]