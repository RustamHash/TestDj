from django.urls import path

from ut import views

urlpatterns = [
    path('', views.index, name='index'),
    path('debit-client/', views.debit_client, name='debit_client'),
    path('debit-provider/', views.debit_provider, name='debit_provider'),
    path('compare-stock/', views.compare_stock, name='compare_stock'),
]
