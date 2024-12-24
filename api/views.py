from django.shortcuts import render
from rest_framework import viewsets, generics

from .models import TestModel
from .serializers import TestSerializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = TestModel.objects.all()
    serializer_class = TestSerializer

