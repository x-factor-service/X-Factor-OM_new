import logging
from datetime import timedelta, datetime
from pprint import pprint

import pandas as pd
from django.core import serializers
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
logger = logging.getLogger(__name__)

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

def deploy(request):
    DCDL = DashboardData()
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        if Customer == 'NC' or Customer == 'Xfactor':
            SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
            SKURL = apiUrl + SesstionKeyPath
            SKR = requests.post(SKURL, data=SKH, verify=False)
            SKRT = SKR.content.decode('utf-8')
            SKRJ = json.loads(SKRT)
            SK = SKRJ['data']['session']

            print("SessionKey 불러오기 성공")

            PSQ = {'session': SK, 'Content-Type': 'application/json'}
            PURL = apiUrl + '/api/v2/packages'
            responsePack = requests.get(PURL, headers=PSQ, verify=False)
            dataP = responsePack.json()
            packageList= []
            groupsList = []
            for i in range(len(dataP['data'])-1):
                if dataP['data'][i]['content_set']['name'] == 'Default':
                    packageList.append({'id': dataP['data'][i]['id'], 'Display_name': dataP['data'][i]['display_name'], 'Content_set': dataP['data'][i]['content_set']['name'],
                                        'Command': dataP['data'][i]['command'], 'Command_Timeout': dataP['data'][i]['command_timeout']})
            # print(data['data'][0]['content_set']['name'])
            GURL = apiUrl + '/api/v2/groups'
            responseGroup = requests.get(GURL, headers=PSQ, verify=False)
            dataG = responseGroup.json()
            # print(dataG['data'][0])
            for i in range(len(dataG['data'])-1):
                groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})

            chartData = {'packageList': packageList, 'groupsList': groupsList}

            returnData = {'menuList': menuListDB, 'chartData': chartData, 'Customer': Customer, 'Login_Method': Login_Method}
        return render(request, 'common/deploy.html', returnData)

def report(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer}
    return render(request, 'common/sbom.html', returnData)

def deploy_action(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer}
    return render(request, 'common/deploy.html', returnData)

@csrf_exempt
def deploy_action_val(request):
    packName = request.POST.get('outputPValue')
    comName = request.POST.get('outputCValue')
    SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    SKURL = apiUrl + SesstionKeyPath
    SKR = requests.post(SKURL, data=SKH, verify=False)
    SKRT = SKR.content.decode('utf-8')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']

    print("SessionKey 불러오기 성공")

    PSQ = {'session': SK, 'Content-Type': 'application/json'}
    PURL = apiUrl + '/api/v2/packages/by-name/' + packName
    CURL = apiUrl + '/api/v2/groups/by-name/' + comName

    PSR = requests.get(PURL, headers=PSQ, verify=False)
    CSR = requests.get(CURL, headers=PSQ, verify=False)

    PSRC = PSR.status_code
    PSRT = PSR.content.decode('utf-8')
    CSRT = CSR.content.decode('utf-8')
    PSRJ = json.loads(PSRT)
    CSRJ = json.loads(CSRT)
    print(PSRJ['data']['id'])
    print(CSRJ['data']['id'])

    print(request.POST.get('outputCValue'))
    aaa = {'aa': aa}
    # posts_serialized = serializers.serialize('json', aa)
    # print(posts_serialized)
    return render(request, 'common/deploy.html', aaa)

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
# def reportdaily(request):
#     returnData = {'menuList': menuListDB, 'Customer': Customer,}
#     return render(request, 'web/report_daily.html', returnData)
#
#
# def reportmonthly(request):
#     returnData = {'menuList': menuListDB, 'Customer': Customer,}
#     return render(request, 'web/report_monthly.html', returnData)

#############################리포트 수정부분 #########################################
def reportdaily(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/report_daily.html', returnData)

def reportPagedaily(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_daily.html', returnData)

def reportPagedaily1(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_daily1.html', returnData)

def reportPagedaily2(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_daily2.html', returnData)

def reportPagedaily3(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_daily3.html', returnData)

def reportPagedaily4(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_daily4.html', returnData)





def reportmonthly(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/report_monthly.html', returnData)

def reportPageweekly(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_weekly.html', returnData)

def reportPageweekly1(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_weekly1.html', returnData)

def reportPageweekly2(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_weekly2.html', returnData)
def reportPageweekly3(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_weekly3.html', returnData)

def reportPageweekly4(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/reportPage_weekly4.html', returnData)
#############################리포트 수정부분 #########################################



def reportannual(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/report_annual.html', returnData)


def ncBanner(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/dashboard_NC_banner.html', returnData)


def customizing(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/customizing.html', returnData)


############################ 팝업 ############################################
