# Generated by Django 3.2.22 on 2023-10-15 23:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0080_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='term',
            options={'ordering': ['term'], 'verbose_name': 'Subcategory', 'verbose_name_plural': 'Subcategories'},
        ),
    ]