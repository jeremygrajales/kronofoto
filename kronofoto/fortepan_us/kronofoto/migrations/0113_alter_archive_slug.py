# Generated by Django 4.2.9 on 2024-05-03 16:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("kronofoto", "0112_alter_archive_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="archive",
            name="slug",
            field=models.SlugField(unique=True),
        ),
    ]