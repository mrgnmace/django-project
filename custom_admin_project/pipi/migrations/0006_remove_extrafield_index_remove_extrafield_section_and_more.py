# Generated by Django 4.2 on 2024-10-02 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipi', '0005_extrafield_index_extrafield_section'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extrafield',
            name='index',
        ),
        migrations.RemoveField(
            model_name='extrafield',
            name='section',
        ),
        migrations.AddField(
            model_name='imagefield',
            name='index',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagefield',
            name='section',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
