# Generated by Django 2.2.5 on 2019-12-29 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movietime', '0011_movie_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('answer', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'FAQ',
            },
        ),
    ]
