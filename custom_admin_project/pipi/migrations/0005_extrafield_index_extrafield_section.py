# Generated by Django 4.2 on 2024-10-02 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipi', '0004_alter_imagefield_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='extrafield',
            name='index',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='extrafield',
            name='section',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
