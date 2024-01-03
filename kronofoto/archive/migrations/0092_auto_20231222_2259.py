# Generated by Django 3.2.22 on 2023-12-22 22:59

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0091_auto_20231218_2251'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(null=True, srid=4326)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='archive.place')),
                ('place_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='archive.placetype')),
            ],
        ),
        migrations.AddIndex(
            model_name='place',
            index=models.Index(fields=['name'], name='archive_pla_name_c28f33_idx'),
        ),
        migrations.AddIndex(
            model_name='place',
            index=models.Index(fields=['place_type', 'name', 'parent'], name='archive_pla_place_t_0a93db_idx'),
        ),
    ]
