from django.shortcuts import render
from rest_framework import viewsets, generics

from .models import TestModel, TestModel2
from .serializers import TestSerializer, TestModel2Serializer


class TestViewSet(viewsets.ModelViewSet):
    queryset = TestModel.objects.all()
    serializer_class = TestSerializer


class TestModel2ViewSet(viewsets.ModelViewSet):
    queryset = TestModel2.objects.all()
    serializer_class = TestModel2Serializer
