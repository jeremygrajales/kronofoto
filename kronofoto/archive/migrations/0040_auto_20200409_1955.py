# Generated by Django 2.2.10 on 2020-04-09 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0039_auto_20200409_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='slug',
            field=models.SlugField(blank=True, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='term',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]