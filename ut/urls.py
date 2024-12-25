from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from ut import views

urlpatterns = [
    path('', csrf_exempt(views.index), name='index'),
    path('debit-client/', csrf_exempt(views.debit_client), name='debit_client'),
    path('debit-provider/', csrf_exempt(views.debit_provider), name='debit_provider'),
    path('compare-stock/', csrf_exempt(views.compare_stock), name='compare_stock'),
]
