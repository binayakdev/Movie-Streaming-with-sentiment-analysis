# Generated by Django 2.2.5 on 2019-12-21 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserSettings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
