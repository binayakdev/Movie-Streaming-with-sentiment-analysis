from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('index', views.index, name='sentiment_index'),
    re_path(r'^analysis/movie_id=(?P<id>\d+)/$', views.analysis, name='analysis')
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
