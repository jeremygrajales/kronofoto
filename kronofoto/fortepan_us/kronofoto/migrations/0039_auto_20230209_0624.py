# Generated by Django 3.2.17 on 2023-02-09 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kronofoto', '0038_alter_photo_tags'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='phototag',
            index=models.Index(fields=['tag', 'photo'], name='archive_pho_tag_id_2ea640_idx'),
        ),
        migrations.AddConstraint(
            model_name='phototag',
            constraint=models.UniqueConstraint(fields=('tag', 'photo'), name='unique_tag_photo'),
        ),
    ]