# Generated by Django 4.2.13 on 2024-10-17 20:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kronofoto', '0122_exhibit_credits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exhibit',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='exhibit',
            name='title',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='figure',
            name='photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kronofoto.photo'),
        ),
        migrations.AlterField(
            model_name='photocard',
            name='photo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='kronofoto.photo'),
        ),
    ]