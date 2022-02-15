# Generated by Django 3.2.8 on 2021-12-16 23:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0030_photosphere_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='photospherepair',
            name='azimuth',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(limit_value=-180), django.core.validators.MaxValueValidator(limit_value=180)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photospherepair',
            name='distance',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(limit_value=1), django.core.validators.MaxValueValidator(limit_value=2000)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photospherepair',
            name='inclination',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(limit_value=-90), django.core.validators.MaxValueValidator(limit_value=90)]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='photosphere',
            name='heading',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(limit_value=0), django.core.validators.MaxValueValidator(limit_value=360)]),
        ),
    ]