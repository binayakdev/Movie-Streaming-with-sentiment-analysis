from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    avatar = models.ImageField(upload_to='avatar')
    bio = models.TextField()
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class SubscriptionPlan(models.Model):
    membership_type = models.CharField(default='Premium', max_length=50)
    membership_description = models.TextField()
    price = models.IntegerField(default=15)
    stripe_plan_id = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.membership_type


class UserSubscription(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=40)
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    stripe_subscription_id = models.CharField(max_length=40)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
