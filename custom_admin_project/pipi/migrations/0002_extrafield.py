# Generated by Django 4.2 on 2024-09-19 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pipi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_value', models.CharField(max_length=255)),
                ('your_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_fields', to='pipi.yourmodel')),
            ],
        ),
    ]
