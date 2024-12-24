from django.db import models


class TestModel(models.Model):
    name = models.CharField(max_length=155)
    age = models.IntegerField()


class TestModel2(models.Model):
    name = models.CharField(max_length=155)
