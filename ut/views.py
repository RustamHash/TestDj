from django.shortcuts import render
from api.models import TestModel


def index(request):
    context = {
        'data': TestModel.objects.all()
    }
    return render(request, 'ut/home.html', context=context)
