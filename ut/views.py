from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import CompareDebitClient

menus = [
    {'id': 1, 'name': 'Сверить долги клиентов', 'url': '/debit-client/', 'as_active': True},
    {'id': 2, 'name': 'Сверить долги поставщиков', 'url': '/debit-provider/', 'as_active': True},
    {'id': 3, 'name': 'Сверить Остатки', 'url': '/compare-stock/', 'as_active': True},
]


# @csrf_exempt
def index(request):
    context = {
        'data': 'Тестовая страница Лепехина',
        'menus': menus
    }
    return render(request, 'ut/home.html', context=context)


def debit_client(request):
    if request.method == 'POST':
        file_ut = request.FILES['file_ut']
        file_bux = request.FILES['file_bux']
        file_name, error_bol = CompareDebitClient(file_ut=file_ut, file_bux=file_bux).start()
        print(f'file_name: {file_name}__error_bol: {error_bol}')
        if error_bol:
            return HttpResponse({'error_msg': file_name, 'error_bol': error_bol})
        else:
            return HttpResponse(f'file_name: {file_name}__error_bol: {error_bol}')
    else:
        context = {
            'menus': menus
        }
        return render(request, 'ut/show_result.html', context=context)


def debit_provider(request):
    if request.method == 'POST':
        file = request.FILES['file']
        context = {
            'file': file,
            'menus': menus
        }
        name = file.name
        return render(request, 'ut/show_result.html', context=context)
    else:
        context = {
            'menus': menus
        }
        return render(request, 'ut/show_result.html', context=context)


def compare_stock(request):
    if request.method == 'POST':
        file = request.FILES['file']
        context = {
            'file': file,
            'menus': menus
        }
        name = file.name
        return render(request, 'ut/show_result.html', context=context)
    else:
        context = {
            'menus': menus
        }
        return render(request, 'ut/show_result.html', context=context)
