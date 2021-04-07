# Generated by Django 2.2.10 on 2021-04-07 21:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0020_auto_20210331_2238'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
