# Generated by Django 4.2 on 2024-10-11 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipi', '0011_alter_accordionitem_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accordionitem',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
    ]
