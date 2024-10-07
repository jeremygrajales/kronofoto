# Generated by Django 3.2.17 on 2023-03-24 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kronofoto', '0054_connecticutrecord_publishable'),
    ]

    operations = [
        migrations.AddField(
            model_name='connecticutrecord',
            name='cleaned_city',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AddField(
            model_name='connecticutrecord',
            name='cleaned_country',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AddField(
            model_name='connecticutrecord',
            name='cleaned_county',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
        migrations.AddField(
            model_name='connecticutrecord',
            name='cleaned_state',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
    ]