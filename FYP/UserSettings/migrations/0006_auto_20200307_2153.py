# Generated by Django 2.2.5 on 2020-03-07 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserSettings', '0005_usersubscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='stripe_plan_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]