import logging
from datetime import timedelta, datetime
from pprint import pprint

import pandas as pd
from django.core import serializers
from django.shortcuts import render, redirect
from sbom.dashboardFunctionSBOM import DashboardData
from common.controller.controllerCommon import MenuSetting
from deploy.transformDeploy import transform as DETR
from deploy.output.deployOutput import plug_in as DEOP
from deploy.input.db import plug_in as DIPI
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

            #print("SessionKey 불러오기 성공")

            PSQ = {'session': SK, 'Content-Type': 'application/json'}
            PURL = apiUrl + '/api/v2/packages'
            responsePack = requests.get(PURL, headers=PSQ, verify=False)
            dataP = responsePack.json()
            packageList= []
            groupsList = []
            # for i in range(len(dataP['data'])-1):
            #     if dataP['data'][i]['content_set']['name'] == 'Default':
            #         packageList.append({'id': dataP['data'][i]['id'], 'Display_name': dataP['data'][i]['display_name'], 'Content_set': dataP['data'][i]['content_set']['name'],
            #                             'Command': dataP['data'][i]['command'], 'Command_Timeout': dataP['data'][i]['command_timeout']})
            # # print(data['data'][0]['content_set']['name'])
            # GURL = apiUrl + '/api/v2/groups'
            # responseGroup = requests.get(GURL, headers=PSQ, verify=False)
            # dataG = responseGroup.json()
            # # print(dataG['data'][0])
            # for i in range(len(dataG['data'])-1):
            #     groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})

            actionLogList = []
            actionLog = DIPI('action_log', '', '')
            for i in range(len(actionLog)):
                actionLogList.append({'package': actionLog[i][0], 'computer_group': actionLog[i][1], 'comment': actionLog[i][2], 'admin': actionLog[i][3], 'creation_date': actionLog[i][4]})

            chartData = {'packageList': packageList, 'groupsList': groupsList, 'actionLogList': actionLogList}
            returnData = {'menuList': menuListDB, 'chartData': chartData, 'Customer': Customer, 'Login_Method': Login_Method}

            request.POST = None
            request._post = None
            request._files = None
        return render(request, 'deploy/deploy.html', returnData)

def report(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer}
    return render(request, 'common/sbom.html', returnData)

def deploy_action(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer}
    return render(request, 'deploy/deploy.html', returnData)

def deploy_action_val(request):
    input_values = []
    ivCnt = 0
    for i in range(1, 100):  # 최대 100개의 인풋 태그를 처리할 수 있도록 범위 설정
        key = 'hiddenn' + str(i)
        value = request.POST.getlist(key)
        if not value:  # 빈 리스트인 경우 루프를 중단
            break
        input_values.extend(value)

    ivCnt = len(input_values)
    print(ivCnt)

    if request.POST.get('outputPValue') == None or request.POST.get('outputCValue') == None or request.POST.get('outputPValue') == '' or request.POST.get('outputCValue') == '':
        print("pass")
        pass
    else:
        packName = request.POST.get('outputPValue')
        print(packName)
        comName = request.POST.get('outputCValue')
        SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
        SKURL = apiUrl + SesstionKeyPath
        SKR = requests.post(SKURL, data=SKH, verify=False)
        SKRT = SKR.content.decode('utf-8')
        SKRJ = json.loads(SKRT)
        SK = SKRJ['data']['session']

        #print("SessionKey 불러오기 성공")

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

        AURL = apiUrl + '/api/v2/actions'
        if not input_values:
            body = {
                "action_group": {
                    "id": 4
                },
                "package_spec": {
                    "id": PSRJ['data']['id']
                },
                "name": "Sample Action",
                "expire_seconds": 3600,
                "target_group": {
                    "id": CSRJ['data']['id']
                }
            }
        else:
            body = {
                "action_group": {
                    "id": 4
                },
                "package_spec": {
                    "source_id": PSRJ['data']['id'],
                    "parameters": []

                },
                "name": "Sample Action",
                "target_group": {
                    "id": CSRJ['data']['id']
                }
            }
            # 포문으로 키와 값을 추가
            for i in range(ivCnt):
                key = f"${i+1}"
                value = input_values[i]
                body["package_spec"]["parameters"].append({"key": key, "value": value})
        print(body)
        CAQ = requests.post(AURL, headers=PSQ, json=body, verify=False)
        if CAQ.status_code == 200:
            DPAD = DETR(CAQ.json(), request.session['sessionid'], 'deploy')
            DEOP(DPAD, 'action_log')

    return redirect('deploy')

@csrf_exempt
def package_paging(request):
    if Customer == 'NC' or Customer == 'Xfactor':
        search = request.POST.get('search')
        con_set = request.POST.get('id')
        if con_set is None:
            con_set = 'Default'
        SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
        SKURL = apiUrl + SesstionKeyPath
        SKR = requests.post(SKURL, data=SKH, verify=False)
        SKRT = SKR.content.decode('utf-8')
        SKRJ = json.loads(SKRT)
        SK = SKRJ['data']['session']

        #print("SessionKey 불러오기 성공")

        PSQ = {'session': SK, 'Content-Type': 'application/json'}
        PURL = apiUrl + '/api/v2/packages'
        responsePack = requests.get(PURL, headers=PSQ, verify=False)
        dataP = responsePack.json()
        packageList = []
        # print(con_set)
        for i in range(len(dataP['data']) - 1):
            if con_set == 'all':
                if dataP['data'][i]['name'].startswith(search) or dataP['data'][i]['content_set']['name'].startswith(search) or dataP['data'][i]['command'].startswith(search):
                    packageList.append({'Name': dataP['data'][i]['name'], 'Content_set': dataP['data'][i]['content_set']['name'],
                                        'Command': dataP['data'][i]['command']})
            elif dataP['data'][i]['content_set']['name'] == con_set and search is None:
                packageList.append({'id': dataP['data'][i]['id'], 'Name': dataP['data'][i]['name'], 'Content_set': dataP['data'][i]['content_set']['name'],
                                    'Command': dataP['data'][i]['command'], 'Command_Timeout': dataP['data'][i]['command_timeout']})
            elif dataP['data'][i]['content_set']['name'] == con_set:
                if dataP['data'][i]['name'].startswith(search) or dataP['data'][i]['content_set']['name'].startswith(search) or dataP['data'][i]['command'].startswith(search):
                    packageList.append({'Name': dataP['data'][i]['name'], 'Content_set': dataP['data'][i]['content_set']['name'],
                                        'Command': dataP['data'][i]['command']})
        Count = len(packageList)
        RD = {'item': packageList,
                'recordsTotal': Count,
                'recordsFiltered': Count,
                }
        return JsonResponse(RD)

@csrf_exempt
def computerGroup_paging(request):
    if Customer == 'NC' or Customer == 'Xfactor':
        search = request.POST.get('search')
        print(search)
        con_set = request.POST.get('id')
        if con_set is None:
            con_set = ''
        SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
        SKURL = apiUrl + SesstionKeyPath
        SKR = requests.post(SKURL, data=SKH, verify=False)
        SKRT = SKR.content.decode('utf-8')
        SKRJ = json.loads(SKRT)
        SK = SKRJ['data']['session']

        #print("SessionKey 불러오기 성공")

        PSQ = {'session': SK, 'Content-Type': 'application/json'}
        PURL = apiUrl + '/api/v2/packages'
        groupsList = []
        # print(data['data'][0]['content_set']['name'])
        GURL = apiUrl + '/api/v2/groups'
        responseGroup = requests.get(GURL, headers=PSQ, verify=False)
        dataG = responseGroup.json()
        # print(dataG['data'][0])


        for i in range(len(dataG['data']) - 1):
            if con_set == 'all':
                if dataG['data'][i]['name'].startswith(search) or dataG['data'][i]['content_set']['name'].startswith(search) or dataG['data'][i]['text'].startswith(search):
                    groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})
            elif dataG['data'][i]['content_set']['name'] == con_set and search is None:
                groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})
            elif dataG['data'][i]['content_set']['name'] == con_set:
                if dataG['data'][i]['name'].startswith(search) or dataG['data'][i]['content_set']['name'].startswith(search) or dataG['data'][i]['text'].startswith(search):
                    groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})

        Count = len(groupsList)
        RD = {'item': groupsList,
              'recordsTotal': Count,
              'recordsFiltered': Count,
              }
        return JsonResponse(RD)


@csrf_exempt
def packCheck(request):
    packName = request.POST.get('id')
    SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    SKURL = apiUrl + SesstionKeyPath
    SKR = requests.post(SKURL, data=SKH, verify=False)
    SKRT = SKR.content.decode('utf-8')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']

    print("SessionKey 불러오기 성공")

    PSQ = {'session': SK, 'Content-Type': 'application/json'}
    PURL = apiUrl + '/api/v2/packages/by-name/' + packName
    responsePack = requests.get(PURL, headers=PSQ, verify=False)
    dataP = responsePack.json()
    # print(dataP['data']['command'])
    a = dataP['data']['command'].count('$')
    print(a)
    RD = {'a': a}

    return JsonResponse(RD)
