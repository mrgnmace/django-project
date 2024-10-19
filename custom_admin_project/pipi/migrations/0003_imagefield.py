# Generated by Django 4.2 on 2024-09-23 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pipi', '0002_extrafield'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('your_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pipi.yourmodel')),
            ],
        ),
    ]
