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
APIUNM = SETTING['API']['username']
APIPWD = SETTING['API']['password']
DEFAULTGROUPID = SETTING['API']['defaultGroupID']
PACKAGEID = SETTING['API']['packageID']
Email_id = SETTING['EMAIL']['EMAIL_ID']
Email_pwd = SETTING['EMAIL']['EMAIL_PWD']

menuListDB = MenuSetting()

# SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
# SKURL = apiUrl + SesstionKeyPath
# SKR = requests.post(SKURL, data=SKH, verify=False)
# SKRT = SKR.content.decode('utf-8')
# SKRJ = json.loads(SKRT)
# SK = SKRJ['data']['session']
#
# print("SessionKey 불러오기 성공")
#
# CSQ = {'session': SK, 'Content-Type': 'application/json'}
# CSURL = apiUrl + '/api/v2/questions'

def sbom(request):
    DCDL = DashboardData()
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        if Customer == 'NC' or Customer == 'Xfactor':

            # sbom_package_list = DCDL['sbom_package_list']
            chartData = {}

            returnData = {'menuList': menuListDB, 'chartData': chartData, 'Customer': Customer, 'Login_Method': Login_Method}
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
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    Data = SDPI('sbom_paging', 'sbom', data)
    print(Data)
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
                            'pv': sbomD[i][3], 'type': sbomD[i][4], 'parent': sbomD[i][5],
                            'count': sbomD[i][6]})
    chartData = {'detail_list': detail_list}
    returnData = {'menuList': menuListDB, 'Customer': Customer, 'chartData': chartData}
    return render(request, 'common/sbom_detail.html', returnData)

@csrf_exempt
def sbom_cve_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [str(length), str(page), str(search)]
    Data = SDPI('sbom_cve', 'cpuMore', data)
    Count = SDPI('sbom_cve_count', '', data)
    RD = {'item': Data}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': Count,
                  'recordsFiltered': Count,
                  }
    return JsonResponse(returnData)








    # SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    # SKURL = apiUrl + SesstionKeyPath
    # SKR = requests.post(SKURL, data=SKH, verify=False)
    # SKRT = SKR.content.decode('utf-8')
    # SKRJ = json.loads(SKRT)
    # SK = SKRJ['data']['session']
    #
    # print("SessionKey 불러오기 성공")
    #
    # CSQ = {'session': SK, 'Content-Type': 'application/json'}
    # CSURL = apiUrl + '/api/v2/questions'
    #
    # CSB = '{"query_text": "Get Computer Name and SBOM Discovered Package Information For CPE[\\"' + value + '\\",0,0,0,0] from all machines"}'
    # CS = requests.post(CSURL, headers=CSQ, data=CSB, verify=False)
    #
    # if CS.status_code == 200:
    #     CSID = str(CS.json()['data']['id'])
    #     print(CSID)
    # sleep(40)
    #
    # SBOMQ = apiUrl + '/api/v2/result_data/question/' + CSID
    # print(SBOMQ)
    #
    # SDList = []
    # response = requests.get(SBOMQ, headers=CSQ, verify=False)
    # if response.status_code == 200:
    #     data = response.json()
    #     columns = [col["name"] for col in data["data"]["result_sets"][0]["columns"]]
    #     rows_data = data["data"]["result_sets"][0]["rows"]
    #     df_data = []
    #     for row in rows_data:
    #         row_data = []
    #         exclude_row = False  # Exclude this row from dataframe or not
    #         for item in row["data"]:
    #             values = [entry["text"] for entry in item]  # Extract all 'text' values from each item
    #             if '[current result unavailable]' in values or '[no results]' in values:
    #                 exclude_row = True  # Set to exclude row if '[current' or '[no' is in values
    #                 break  # No need to process this row further, so break from inner loop
    #             row_data.append(', '.join(values))  # Join the extracted values with ', '
    #         if not exclude_row:
    #             df_data.append(row_data)
    #     df = pd.DataFrame(df_data, columns=columns)
    #     pd.set_option('display.expand_frame_repr', False)
    #     print(df)
    #     for i in range(len(df)):
    #         if df['Name'][i] == 'Not Scanned' or df['Name'][i] == 'No Packages Found':
    #             continue
    #         else:
    #             SDList.append({'cn': df['Computer Name'][i], 'pn': df['Name'][i], 'pv': df['Version'][i], 'type': df['Type'][i], 'parent': df['Parent'][i], 'count': df['Count'][i]})
    # print('GET 요청 실패: ', response.status_code)
    chartData = {'detail_list': detail_list}
    returnData = {'menuList': menuListDB, 'Customer': Customer, 'chartData': chartData}
    return render(request, 'sbom/sbom_detail.html', returnData)

# @csrf_exempt
# def sbom_detail_paging(request):
#     print(request.GET.get('cpe'))
#     print(request.method)
#     print(request.path)
#     SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
#     SKURL = apiUrl + SesstionKeyPath
#     SKR = requests.post(SKURL, data=SKH, verify=False)
#     SKRT = SKR.content.decode('utf-8')
#     SKRJ = json.loads(SKRT)
#     SK = SKRJ['data']['session']
#     print("SessionKey 불러오기 성공")
#     a = 'cpe:2.3:a:slf4j-api:slf4j-api:1.7.25:*:*:*:*:*:*:*'
#     CSQ = {'session': SK, 'Content-Type': 'application/json'}
#     CSURL = apiUrl + '/api/v2/questions'
#     CSB = '{"query_text": "Get Computer Name and SBOM Discovered Package Information For CPE[\\"' + a + '\\",0,0,0,0] from all machines"}'
#     CS = requests.post(CSURL, headers=CSQ, data=CSB, verify=False)
#     print("success")
#     CSID = str(CS.json()['data']['id'])
#     print(CSID)
#     SBOMQ = apiUrl + '/api/v2/result_data/question/'+CSID
#     sleep(10)
#     response = requests.get(SBOMQ, headers=CSQ, verify=False)
#     # print(response.json())
#     aaa = request.GET.get('cpe')
#     # print(aaa)
#     if response.status_code == 200:
#         data = response.json()
#         columns = [col["name"] for col in data["data"]["result_sets"][0]["columns"]]
#         rows_data = data["data"]["result_sets"][0]["rows"]
#         df_data = []
#         for row in rows_data:
#             row_data = []
#             exclude_row = False  # Exclude this row from dataframe or not
#             for item in row["data"]:
#                 values = [entry["text"] for entry in item]  # Extract all 'text' values from each item
#                 if '[current result unavailable]' in values or '[no results]' in values:
#                     exclude_row = True  # Set to exclude row if '[current' or '[no' is in values
#                     break  # No need to process this row further, so break from inner loop
#                 row_data.append(', '.join(values))  # Join the extracted values with ', '
#             if not exclude_row:
#                 df_data.append(row_data)
#         df = pd.DataFrame(df_data, columns=columns)
#         pd.set_option('display.expand_frame_repr', False)
#     else:
#         print('GET 요청 실패: ', response.status_code)

    # draw = int(request.POST.get('draw'))
    # start = int(request.POST.get('start'))
    # length = int(request.POST.get('length'))
    # search = request.POST.get('search[value]')
    # page = math.ceil(start / length) + 1
    # data = [str(length), str(page), str(search)]
    # Data = SDPI('sbom_paging', 'sbom', data)
    # Count = SDPI('sbom_paging_count', '', data)
    # RD = {'item': Data}
    # returnData = {'data': RD,
    #               'draw': draw,
    #               'recordsTotal': Count,
    #               'recordsFiltered': Count,
    #               }
    # return



############################ 팝업 ############################################
