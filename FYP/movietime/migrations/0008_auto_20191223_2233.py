# Generated by Django 2.2.5 on 2019-12-23 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movietime', '0007_genre'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='genre',
            new_name='genre_name',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(related_name='genre', to='movietime.Genre'),
        ),
    ]
