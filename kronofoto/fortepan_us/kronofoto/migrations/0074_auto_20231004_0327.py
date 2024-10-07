# Generated by Django 3.2.21 on 2023-10-04 03:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('kronofoto', '0073_alter_photosphere_links'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchiveGroupPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kronofoto.archive')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.group')),
                ('permission', models.ManyToManyField(to='auth.Permission')),
            ],
            options={
                'verbose_name': 'archive',
                'verbose_name_plural': 'archive permissions',
            },
        ),
        migrations.AddIndex(
            model_name='archivegrouppermission',
            index=models.Index(fields=['archive', 'group'], name='archive_arc_archive_311fbb_idx'),
        ),
        migrations.AddConstraint(
            model_name='archivegrouppermission',
            constraint=models.UniqueConstraint(fields=('archive', 'group'), name='unique_archive_group'),
        ),
    ]