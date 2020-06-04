from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views as user_views

# These are the URL patterns for the UserSettings app

urlpatterns = [
    path('review-subscription/type=<slug:subscription_type>',
         user_views.review_subscription, name='review_subscription'),
    path('register/editplan', user_views.choose_plan, name='choose_plan'),
    path('register/plan=<slug:plan>', user_views.register, name='register'),
    path('login/', user_views.login, name='login'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='logout.html'), name='logout'),
    path('upgrade-plan', user_views.upgrade_account, name='upgrade_account'),
    path('upgrade', user_views.upgrade, name='upgrade'),
    path('reset-password', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('reset-password/done', auth_views.PasswordResetDoneView.as_view(template_name='reset_done.html'),
         name='password_reset_done'),
    re_path(r'^reset-password/cofirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(template_name='reset_confirm.html'),
            name='password_reset_confirm'),
    path('reset-password/complete', auth_views.PasswordResetCompleteView.as_view(template_name='reset_complete.html'),
         name='password_reset_complete'),
    path('profile', user_views.profile, name='profile'),
    path('profile/edit', user_views.edit_profile, name='edit_profile'),
    path('profile/change-password',
         user_views.change_password, name='change_password'),
    path('profile/settings', user_views.settings, name="settings_profile"),
    path('profile/delete', user_views.del_user, name="delete_profile"),
    path('profile/cancel-subscription',
         user_views.cancel_subscription, name="cancel_subscription"),
    path('profile/activate-subscription',
         user_views.reactivate_subscription, name="reactivate_subscription"),
]
