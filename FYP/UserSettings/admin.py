from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .forms import UserRegisterForm, CustomUserChangeForm
from .models import Profile, SubscriptionPlan, UserSubscription

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    model = Profile
    list_display = ['username', 'avatar']


# Registering the models in the superuser panel
admin.site.register(Profile, CustomUserAdmin)
admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
