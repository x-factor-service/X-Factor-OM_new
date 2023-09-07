from datetime import timedelta, datetime
from pprint import pprint

import pandas as pd
from django.shortcuts import render, redirect
from sbom.dashboardFunctionSBOM import DashboardData
from common.controller.controllerCommon import MenuSetting
from om.input.db import plug_in as PDPI
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from sbom.input.db import plug_in as SDPI
import requests
import smtplib
import json
import math

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
Customer = SETTING['PROJECT']['CUSTOMER']
WorldUse = SETTING['PROJECT']['MAP']['World']
KoreaUse = SETTING['PROJECT']['MAP']['Korea']
AreaUse = SETTING['PROJECT']['MAP']['Area']['use']
AreaType = SETTING['PROJECT']['MAP']['Area']['type']
Login_Method = SETTING['PROJECT']['LOGIN']
apiUrl = SETTING['API']['apiUrl']
SesstionKeyPath = SETTING['API']['PATH']['SessionKey']

menuListDB = MenuSetting()

def sbom(request):
    DCDL = DashboardData()
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        sbom_pieData = DCDL["sbom_pieData"]
        sbom_lineData = DCDL["sbom_lineData"]
        sbom_barData = DCDL["sbom_barData"]
        sbomDataList = {"sbom_pieData": sbom_pieData, "sbom_lineData": sbom_lineData ,"sbom_barData": sbom_barData}
        returnData = {'menuList': menuListDB, 'sbomDataList': sbomDataList, 'Customer': Customer, 'Login_Method': Login_Method}
        return render(request, 'sbom/sbom.html', returnData)

def report(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer}
    return render(request, 'sbom/sbom.html', returnData)

@csrf_exempt
def sbom_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    search_values = search.split('||')
    search_1 = search_values[0]
    if len(search_values) > 1:
        search_2 = search_values[1]
    else:
        search_2 = ""
    order_column = int(request.POST.get('order[0][column]'))
    order_direction = request.POST.get('order[0][dir]')

    page = math.ceil(start / length) + 1
    data = [str(length), str(page), str(search_1), str(search_2), order_column, order_direction]
    Data = SDPI('sbom_paging', 'sbom', data)
    Count = SDPI('sbom_paging_count', '', data)
    RD = {'item': Data}
    returnData = {'data': RD,
                    'draw': draw,
                    'recordsTotal': Count,
                    'recordsFiltered': Count,
                    }
    return JsonResponse(returnData)

def sbom_detail(request):
    response = request.GET.get('cpe')
    sbomD = SDPI('sbom_detail', '', response)
    detail_list = []
    for i in range(len(sbomD)):
        detail_list.append({'cn': sbomD[i][0], 'ip': sbomD[i][1], 'pn': sbomD[i][2],
                            'pv': sbomD[i][3], 'type': sbomD[i][4],
                            'count': sbomD[i][5]})
    chartData = {'detail_list': detail_list}
    returnData = {'menuList': menuListDB, 'Customer': Customer, 'chartData': chartData}
    return render(request, 'sbom/sbom_detail.html', returnData)

@csrf_exempt
def sbom_cve_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    order_column = int(request.POST.get('order[0][column]'))
    order_direction = request.POST.get('order[0][dir]')

    page = math.ceil(start / length) + 1
    data = [str(length), str(page), str(search), order_column, order_direction]
    Data = SDPI('sbom_cve', 'sbom_cve', data)
    Count = SDPI('sbom_cve_count', '', data)
    RD = {'item': Data}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': Count,
                  'recordsFiltered': Count,
                  }
    return JsonResponse(returnData)

@csrf_exempt
def cve_in_sbom(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    order_column = int(request.POST.get('order[0][column]'))
    order_direction = request.POST.get('order[0][dir]')
    page = math.ceil(start / length) + 1
    data = [str(length), str(page), str(search), order_column, order_direction]
    Data = SDPI('cve_in_sbom', 'cve_in_sbom', data)
    Count = SDPI('cve_in_sbom_count', '', data)

    RD = {'item': Data}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': Count,
                  'recordsFiltered': Count,
                  }
    return JsonResponse(returnData)

@csrf_exempt
def sbom_in_cve(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    order_column = int(request.POST.get('order[0][column]'))
    order_direction = request.POST.get('order[0][dir]')

    page = math.ceil(start / length) + 1
    data = [str(length), str(page), str(search), order_column, order_direction]
    Data = SDPI('sbom_in_cve', 'sbom_in_cve', data)
    Count = SDPI('sbom_in_cve_count', '', data)
    RD = {'item': Data}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': Count,
                  'recordsFiltered': Count,
                  }
    return JsonResponse(returnData)

@csrf_exempt
def cve_detail(request) :
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            cve_id = request.POST.get('cve_id')
            comp_name = request.POST.get('comp_name')
            comp_ver = request.POST.get('comp_ver')
            draw = int(request.POST.get('draw'))
            start = int(request.POST.get('start'))
            length = int(request.POST.get('length'))
            search = request.POST.get('search[value]')
            page = math.ceil(start / length) + 1
            order_column = int(request.POST.get('order[0][column]'))
            order_direction = request.POST.get('order[0][dir]')

            asset_data = [cve_id, comp_name, comp_ver, str(length), str(page), str(search), order_column, order_direction]
            assetData = SDPI('asset_detail', 'asset_detail', asset_data)
            Count = SDPI('asset_detail_count', '', asset_data)

            RD = {'assetItem': assetData}
            returnData = {'data': RD,
                          'draw': draw,
                          'recordsTotal': Count,
                          'recordsFiltered': Count,
                          }
            return JsonResponse(returnData)
        else:
            cve_id = request.GET.get('cve_id')
            comp_name = request.GET.get('comp_name')
            comp_ver = request.GET.get('comp_ver')
            cve_data = [cve_id, comp_name, comp_ver]
            cveData = SDPI('cve_detail', 'cve_detail', cve_data)
            RD = {'cveItem': cveData}
            returnData = {'data': RD}
            return render(request, 'sbom/cve_detail.html', returnData)