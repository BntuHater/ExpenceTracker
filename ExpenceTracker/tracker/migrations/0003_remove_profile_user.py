# Generated by Django 3.0.2 on 2020-01-18 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]
