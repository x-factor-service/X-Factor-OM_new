import logging
from datetime import timedelta, datetime
from pprint import pprint
import threading
import pytz
import pandas as pd
from django.core import serializers
from django.shortcuts import render, redirect
from sbom.dashboardFunctionSBOM import DashboardData
from common.controller.controllerCommon import MenuSetting
from deploy.transformDeploy import transform as DETR
from deploy.output.deployOutput import plug_in as DEOP
from deploy.output.deployOutput import deploy_status as DSOP
from deploy.input.db import plug_in as DIPI
from om.input.db import plug_in as PDPI
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from sbom.input.db import plug_in as SDPI
import requests
from django.http import HttpResponseRedirect
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
            SKRT = SKR.content.decode('utf-8', errors='ignore')
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
            # ======================action_status data 가져오기 ================
            action_status_List = []
            action_status_Data = DIPI('action_status', '', '')

            for i in range(len(action_status_Data)):
                action_status_List.append({
                    'packageName': action_status_Data[i][0],
                    'action_date': action_status_Data[i][2],
                    'action_status': eval(action_status_Data[i][4]),
                    'action_result': eval(action_status_Data[i][3])
                })


            chartData = {'packageList': packageList, 'groupsList': groupsList, 'actionLogList': actionLogList, 'actionStatusList': action_status_List}

            pre_redirect_data = request.session.get('pre_redirect_data', None)

            if pre_redirect_data is not None:
                chartData['preRedirectData'] = pre_redirect_data
                del request.session['pre_redirect_data']

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
    #print(ivCnt)

    if request.POST.get('outputPValue') == None or request.POST.get('outputCValue') == None or request.POST.get('outputPValue') == '' or request.POST.get('outputCValue') == '':
        #print("pass")
        pass
    else:
        packName = request.POST.get('outputPValue')
        #print(packName)
        comName = request.POST.get('outputCValue')
        SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
        SKURL = apiUrl + SesstionKeyPath
        SKR = requests.post(SKURL, data=SKH, verify=False)
        SKRT = SKR.content.decode('utf-8', errors='ignore')
        SKRJ = json.loads(SKRT)
        SK = SKRJ['data']['session']

        #print("SessionKey 불러오기 성공")

        PSQ = {'session': SK, 'Content-Type': 'application/json'}
        PURL = apiUrl + '/api/v2/packages/by-name/' + packName
        CURL = apiUrl + '/api/v2/groups/by-name/' + comName

        PSR = requests.get(PURL, headers=PSQ, verify=False)
        CSR = requests.get(CURL, headers=PSQ, verify=False)

        PSRC = PSR.status_code
        PSRT = PSR.content.decode('utf-8', errors='ignore')
        CSRT = CSR.content.decode('utf-8', errors='ignore')
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
        #print(body)
        CAQ = requests.post(AURL, headers=PSQ, json=body, verify=False)
        if CAQ.status_code == 200:
            DPAD = DETR(CAQ.json(), request.session['sessionid'], 'deploy')
            DEOP(DPAD, 'action_log')
            result = CAQ.json()
            # # ########################test용 computer group total count 계산 #################################
            # TCG = CSRJ['data']['text']
            # JURL = apiUrl + '/api/v2/questions'
            # body = {
            #     "query_text": "Get Computer Name and IP Address from all machines with ( All Computers and All Computers and " + TCG + ")"
            # }
            # JQP = requests.post(JURL, headers=PSQ, json=body, verify=False)
            # JQPR = JQP.json()
            # JCGI = JQPR['data']['id']
            # JTCURL = apiUrl + '/api/v2/result_data/question/' + str(JCGI)
            # for i in range(5):
            #     sleep(1)
            #
            #     CGRD = requests.get(JTCURL, headers=PSQ, verify=False)
            #     CGTC = CGRD.json()
            #     CGTCR = CGTC['data']['result_sets'][0]['row_count_machines']
            #
            # ###############################
            # 여기서 부터 테스트 시작
            # package name 추출
            pn = result['data']['package_spec']['name']

            # action id 추출
            action_id = result['data']['id']

            # 실행 시간 추출
            U_date = result['data']['package_spec']['creation_time']
            parsed_date = datetime.strptime(U_date, '%Y-%m-%dT%H:%M:%Sz')

            utc_tz = pytz.timezone('UTC')
            kr_tz = pytz.timezone('Asia/Seoul')

            utc_datetime = utc_tz.localize(parsed_date)
            kr_datetime = utc_datetime.astimezone(kr_tz)

            action_date = kr_datetime.strftime('%Y-%m-%d %H:%M:%S')

            AJURL = apiUrl + '/api/v2/result_data/action/' + str(action_id)

            # 완료 시점 체크를 위해 만든 반복 구간 12초에 한번씩 반복
            # 주석처리 부분을 살리면 이중 체크 데이터가 그전 데이터와 일치 할 때 반복 종료 sleep 시간을 많이 안준다면 필요

            prev_rows = None
            while True:
                sleep(12)
                AJ = requests.get(AJURL, headers=PSQ, verify=False)
                AJD = AJ.json()

                rows = AJD['data']['result_sets'][0]['rows']

                if rows and all(row['data'][1][0]['text'] and 'Running.' not in row['data'][1][0][
                    'text'] and 'Downloading.' not in row['data'][1][0]['text'] for row in rows):
                    # break

                    current_rows = AJD['data']['result_sets'][0]['rows']

                    if prev_rows is not None and current_rows and prev_rows == current_rows:
                        break
                    prev_rows = current_rows if current_rows else prev_rows

            ################# action result ##################
            action_result = []
            # DB 용 데이터 가공
            for i in range(len(AJD['data']['result_sets'][0]['rows']) + 1):
                try:
                    key = AJD['data']['result_sets'][0]['rows'][i]['data'][0][0]['text']
                    value = AJD['data']['result_sets'][0]['rows'][i]['data'][1][0]['text'].split(':')

                    action_result.append({key: value[1]})
                except (IndexError, KeyError):
                    pass

            completed_count = 0
            failed_count = 0


            for result in action_result:
                status = next(iter(result.values()))

                if status == 'Completed.':
                    completed_count += 1
                elif status == 'Failed.' or status == 'Expired.':
                    failed_count += 1

            total_count = completed_count + failed_count
            completed_per = str(int((completed_count / total_count) * 100)) + '%'
            failed_per = str(100 - int(completed_per.rstrip('%'))) + '%'


            BData = [completed_per, failed_per]

            ASdata = [pn, action_id, action_date, action_result, BData]
            DSOP(ASdata)
            # print(AJD['data']['result_sets'][0]['rows'][0]['data'][0][0])
            # print(AJD['data']['result_sets'][0]['rows'][0]['data'][1][0])
            # print(AJD['data']['result_sets'][0]['rows'][1]['data'][0][0])
            # print(AJD['data']['result_sets'][0]['rows'][1]['data'][1][0])
            # #######################!111111111111111111111##########################
            # total = 0
            # i = 0
            # while total < CGTCR:
            #     sleep(1)
            #     AJ = requests.get(AJURL, headers=PSQ, verify=False)
            #     AJD = AJ.json()
            #     try:
            #         value1 = AJD['data']['result_sets'][0]['rows'][i]['data']
            #         print(value1)
            #         value = int(AJD['data']['result_sets'][0]['rows'][i]['data'][2][0]['text'])
            #         total += value
            #         print(total)
            #         i += 1
            #     except:
            #         print('아직')
            # print(AJD['data']['result_sets'][0]['rows'])
            # print(action_id)
            ########################22222222222222222222222222#######################
            # total = 0
            # for i in range(10):
            #     while total < CGTCR:
            #         sleep(2)
            #         AJ = requests.get(AJURL, headers=PSQ, verify=False)
            #         AJD = AJ.json()
            #         # print(AJD)
            #
            #         # Ensure the data exists before trying to access it
            #         if len(AJD['data']['result_sets'][0]['rows']) > i:
            #             value = int(AJD['data']['result_sets'][0]['rows'][i]['data'][2][0]['text'])
            #             print(AJD['data']['result_sets'][0]['rows'][i])
            #             print(value)
            #             total += value
            #             print(total)
            RD = {'per': BData}
            return JsonResponse(RD)







@csrf_exempt
def package_paging(request):
    if Customer == 'NC' or Customer == 'Xfactor':
        search = request.POST.get('search').lower()
        con_set = request.POST.get('id')
        if con_set is None:
            con_set = 'X-Factor'
        SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
        SKURL = apiUrl + SesstionKeyPath
        SKR = requests.post(SKURL, data=SKH, verify=False)
        SKRT = SKR.content.decode('utf-8', errors='ignore')
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
                if search in dataP['data'][i]['name'].lower() or search in dataP['data'][i]['content_set']['name'].lower() or search in dataP['data'][i]['command'].lower():
                    packageList.append({'Name': dataP['data'][i]['name'], 'Content_set': dataP['data'][i]['content_set']['name'],
                                        'Command': dataP['data'][i]['command']})
            elif dataP['data'][i]['content_set']['name'] == con_set and search is None:
                packageList.append({'id': dataP['data'][i]['id'], 'Name': dataP['data'][i]['name'], 'Content_set': dataP['data'][i]['content_set']['name'],
                                    'Command': dataP['data'][i]['command'], 'Command_Timeout': dataP['data'][i]['command_timeout']})
            elif dataP['data'][i]['content_set']['name'] == con_set:
                if search in dataP['data'][i]['name'].lower() or search in dataP['data'][i]['content_set']['name'].lower() or search in dataP['data'][i]['command'].lower():
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
        search = request.POST.get('search').lower()
        #print(search)
        con_set = request.POST.get('id')
        if con_set is None:
            con_set = ''
        SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
        SKURL = apiUrl + SesstionKeyPath
        SKR = requests.post(SKURL, data=SKH, verify=False)
        SKRT = SKR.content.decode('utf-8', errors='ignore')
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
                if search in dataG['data'][i]['name'].lower() or search in dataG['data'][i]['content_set']['name'].lower() or search in dataG['data'][i].get('text', '').lower():
                    groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i].get('text', '')})
            elif dataG['data'][i]['content_set']['name'] == con_set and search is None:
                groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i].get('text', '')})
            elif dataG['data'][i]['content_set']['name'] == con_set:
                if search in dataG['data'][i]['name'].lower() or search in dataG['data'][i]['content_set']['name'].lower() or search in dataG['data'][i].get('text', '').lower():
                    groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i].get('text', '')})

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
    SKRT = SKR.content.decode('utf-8', errors='ignore')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']

    #print("SessionKey 불러오기 성공")

    PSQ = {'session': SK, 'Content-Type': 'application/json'}
    PURL = apiUrl + '/api/v2/packages/by-name/' + packName
    responsePack = requests.get(PURL, headers=PSQ, verify=False)
    dataP = responsePack.json()
    # print(dataP['data']['command'])
    a = dataP['data']['command'].count('$')
    #print(a)
    RD = {'a': a}

    return JsonResponse(RD)
