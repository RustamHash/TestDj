from django.urls import path

from ut import views

urlpatterns = [
    path('', views.index, name='index'),
    path('compare-files/', views.compare, name='compare_files'),
]
