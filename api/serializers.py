from rest_framework import serializers
from .models import TestModel, TestModel2


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = '__all__'


class TestModel2Serializer(serializers.ModelSerializer):
    class Meta:
        model = TestModel2
        fields = '__all__'
