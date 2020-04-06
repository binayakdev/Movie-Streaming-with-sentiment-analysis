# Generated by Django 2.2.5 on 2019-12-28 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movietime', '0010_remove_movie_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='genre', to='movietime.Genre'),
        ),
    ]