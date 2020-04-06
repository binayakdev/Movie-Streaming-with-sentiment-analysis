"""FYP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import handler404, handler500
from movietime import views as movietime_views

urlpatterns = [
    path('admin/', include('Admin.urls')),
    path('superuser/', admin.site.urls),
    path('', include('movietime.urls')),
    path('sentiment/', include('sentiment.urls')),
    path('accounts/', include('UserSettings.urls')),
]

handler404 = movietime_views.handler404
handler500 = movietime_views.handler500