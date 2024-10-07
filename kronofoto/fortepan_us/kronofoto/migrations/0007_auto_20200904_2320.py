# Generated by Django 2.2.10 on 2020-09-04 23:20

import fortepan_us.kronofoto.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kronofoto', '0006_auto_20200827_0209'),
    ]

    operations = [
        #migrations.AlterField(
        #    model_name='phototag',
        #    name='creator',
        #    field=models.ManyToManyField(editable=False, to=settings.AUTH_USER_MODEL),
        #),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=fortepan_us.kronofoto.models.LowerCaseCharField(max_length=64, unique=True),
        ),
    ]