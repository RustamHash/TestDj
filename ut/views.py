from django.shortcuts import render
from api.models import TestModel
from tkinter import filedialog

test = False


def index(request):
    context = {
        'data': TestModel.objects.all()
    }
    if test:
        f = filedialog.askopenfilename()
    return render(request, 'ut/home.html', context=context)
