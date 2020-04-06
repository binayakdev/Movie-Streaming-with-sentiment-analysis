# Generated by Django 2.2.5 on 2020-03-07 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UserSettings', '0004_subscriptionplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(max_length=40)),
                ('stripe_subscription_id', models.CharField(max_length=40)),
                ('active', models.BooleanField(default=True)),
                ('subscription_plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UserSettings.SubscriptionPlan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]