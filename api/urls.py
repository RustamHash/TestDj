from django.urls import path, include
from rest_framework import routers
from .views import TestViewSet, TestModel2ViewSet

router = routers.SimpleRouter()
router.register(r'test', TestViewSet)
router.register(r'test2', TestModel2ViewSet)
urlpatterns = [
    path('', include(router.urls))
]
