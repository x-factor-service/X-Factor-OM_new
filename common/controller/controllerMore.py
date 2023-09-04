from django.http import JsonResponse
from django.shortcuts import render
import math
from django.views.decorators.csrf import csrf_exempt

from common.input.db import plug_in as PDPI

# def certificate_more(request) :
#     return render(request, 'common/popup/certificate_more.html')
# @csrf_exempt
# def certificate_more_paging(request):
#     id = request.POST.get('id')
#     draw = int(request.POST.get('draw'))
#     start = int(request.POST.get('start'))
#     length = int(request.POST.get('length'))
#     search = request.POST.get('search[value]')
#     page = math.ceil(start / length) + 1
#     data = [ str(length), str(page), str(search), str(id)]
#     SMD = PDPI('cert_listDataMore', data)
#     SMC = PDPI('cert_listDataMoreCount', data)
#     RD = {"item": SMD}
#     returnData = {'data': RD,
#                   'draw': draw,
#                   'recordsTotal': SMC,
#                   'recordsFiltered': SMC,
#                   }
#     return JsonResponse(returnData)

def highCpuProc_more(request) :
    return render(request, 'common/popup/highCpuProc_more.html')

def highMemProc_more(request) :
    return render(request, 'common/popup/highMemProc_more.html')

def highDiskApp_more(request) :
    return render(request, 'common/popup/highDiskApp_more.html')

@csrf_exempt
def highCpuProc_more_paging(request):
    id = request.POST.get('id')
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [str(length), str(page), str(search), str(id)]
    SMD = PDPI('highCpuProc_listDataMore', data)
    SMC = PDPI('highCpuProc_listDataMoreCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

@csrf_exempt
def highMemProc_more_paging(request):
    id = request.POST.get('id')
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [str(length), str(page), str(search), str(id)]
    SMD = PDPI('highMemProc_listDataMore', data)
    SMC = PDPI('highMemProc_listDataMoreCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

@csrf_exempt
def highDiskApp_more_paging(request):
    id = request.POST.get('id')
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [str(length), str(page), str(search), str(id)]
    SMD = PDPI('highDiskApp_listDataMore', data)
    SMC = PDPI('highDiskApp_listDataMoreCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)