# Generated by Django 2.2.10 on 2020-04-08 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0033_auto_20200406_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField()),
            ],
        ),
        migrations.RemoveField(
            model_name='photo',
            name='proposed_tags',
        ),
        migrations.AlterField(
            model_name='photo',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='archive.Contributor'),
        ),
        migrations.RemoveField(
            model_name='photo',
            name='tags',
        ),
        migrations.AddField(
            model_name='photo',
            name='tags',
            field=models.ManyToManyField(blank=True, through='archive.PhotoTag', to='archive.Tag'),
        ),
        migrations.AddField(
            model_name='phototag',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.Photo'),
        ),
        migrations.AddField(
            model_name='phototag',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='archive.Tag'),
        ),
    ]