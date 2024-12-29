from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import CompareDebitClient, CompareDebitProvider, CompareStock
import logging

logger = logging.getLogger(__name__)

menus = [
    {'id': 1, 'name': 'Сверить долги клиентов', 'url': 'debit-client', 'as_active': True},
    {'id': 2, 'name': 'Сверить долги поставщиков', 'url': 'debit-provider', 'as_active': True},
    {'id': 3, 'name': 'Сверить Остатки', 'url': 'compare-stock', 'as_active': True},
]

apps = {
    'debit-client': CompareDebitClient,
    'debit-provider': CompareDebitProvider,
    'compare-stock': CompareStock,
}


@csrf_exempt
def index(request):
    logger.debug('index')
    context = {
        'form_active': False,
        'menus': menus
    }
    return render(request, 'ut/home.html', context=context)


@csrf_exempt
def compare(request):
    operation = request.GET.get('operation')
    logger.info(f'compare: {operation}')
    context = {
        'form_active': True,
        'menus': menus,
        'operation': operation,
    }
    if request.method == 'POST':
        logger.info(f'method:post:{request.method}')
        file_ut = request.FILES['file_ut']
        logger.info(f'file_ut:{file_ut}')
        file_bux = request.FILES['file_bux']
        logger.info(f'file_bux:{file_bux}')
        file_name, error_bol = apps[operation](file_ut=file_ut, file_bux=file_bux).start()
        logger.info(f'file_name:{file_name}__error_bol:{error_bol}')
        if error_bol:
            logger.error(f'error_bol:{error_bol}, file_name:{file_name}')
            return HttpResponse({'error_msg': file_name, 'error_bol': error_bol})
        else:
            logger.info(f'file_name:{file_name}__error_bol:{error_bol}')
            return FileResponse(open(file_name, 'rb'))
    else:
        logger.info(f'return file')
        return render(request, 'ut/home.html', context=context)
