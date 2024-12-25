import os

import pandas as pd
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import CompareDebitClient
from wms.models import WmsKrd
from ut.models import StockWms

menus = [
    {'id': 1, 'name': 'Сверить долги клиентов', 'url': '/debit-client/', 'as_active': True},
    {'id': 2, 'name': 'Сверить долги поставщиков', 'url': '/debit-provider/', 'as_active': True},
    {'id': 3, 'name': 'Сверить Остатки', 'url': '/compare-stock/', 'as_active': True},
    {'id': 4, 'name': 'Получить остатки из вмс', 'url': '/get-stock-wms/', 'as_active': False},
]


@csrf_exempt
def index(request):
    context = {
        'data': 'Тестовая страница Лепехина',
        'menus': menus
    }
    return render(request, 'ut/home.html', context=context)


@csrf_exempt
def debit_client(request):
    if request.method == 'POST':
        file_ut = request.FILES['file_ut']
        file_bux = request.FILES['file_bux']
        file_name, error_bol = CompareDebitClient(file_ut=file_ut, file_bux=file_bux).start()
        if error_bol:
            return HttpResponse({'error_msg': file_name, 'error_bol': error_bol})
        else:
            print(file_name)
            return FileResponse(open(file_name, 'rb'))
    else:
        context = {
            'menus': menus
        }
        return render(request, 'ut/show_result.html', context=context)


@csrf_exempt
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


@csrf_exempt
def compare_stock(request):
    if request.method == 'POST':
        file = request.FILES['file']
        context = {
            'file': file,
            'menus': menus
        }
        return render(request, 'ut/show_result.html', context=context)
    else:
        context = {
            'menus': menus
        }
        return render(request, 'ut/show_result.html', context=context)


@csrf_exempt
def get_stock(request):
    wms = WmsKrd()
    _df = wms.start()
    df = pd.DataFrame(columns=['Склад', 'Артикул', 'Наименование', 'Дата Производства', 'Годен До', 'Количество'])
    df['Склад'] = _df['ЯчейкаХранения.Склад.Description']
    df['Артикул'] = _df['Номенклатура.Артикул']
    df['Наименование'] = _df['Номенклатура.Description']
    df['Дата Производства'] = _df['СерияНоменклатуры.ДатаПроизводства']
    df['Годен До'] = _df['СерияНоменклатуры.ГоденДо']
    df['Количество'] = _df['КоличествоBalance']
    df.sort_values(by=['Склад', 'Артикул', 'Годен До'], ascending=[True, True, True], inplace=True, ignore_index=True)
    context = {'data': df.to_html(), 'menus': menus}
    path_save_file = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', 'Остатки ВМС.xlsx')
    path_save_file = 'media/Остатки ВМС.xlsx'
    df.to_excel('media/Остатки ВМС.xlsx')
    stock_wms = StockWms.objects.get(id=1)
    stock_wms.file_name = path_save_file
    return render(request, 'ut/show_result.html', context=context)


def get_stock_wms(request):
    stock_wms = StockWms.objects.all()
