from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views as user_views

urlpatterns = [
    path('', user_views.index, name='admin-index'),
    path('login', user_views.admin_login,  name='admin-login'),
    path('register', user_views.admin_register, name='admin-register'),
    path('logout', auth_views.LogoutView.as_view(
        template_name='admin-logout.html'), name='admin-logout'),
    path('admin-users', user_views.admin_users, name='admin-users'),
    path('admin-movies', user_views.admin_movies, name='admin-movies'),
    path('admin-subscribers', user_views.admin_subscribers, name='admin-subscribers'),
    path('admin-stripe', user_views.admin_stripe, name='admin-stripe'),
]
