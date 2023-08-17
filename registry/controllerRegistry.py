import base64
import logging
from pprint import pprint

from django.shortcuts import render, redirect
from common.controller.controllerCommon import MenuSetting
from deploy.transformDeploy import transform as DETR
from deploy.output.deployOutput import plug_in as DEOP
from deploy.input.db import plug_in as DIPI
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

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


def registry(request):
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

            actionLogList = []
            actionLog = DIPI('action_log', '', '')
            for i in range(len(actionLog)):
                actionLogList.append({'package': actionLog[i][0], 'computer_group': actionLog[i][1], 'comment': actionLog[i][2], 'admin': actionLog[i][3], 'creation_date': actionLog[i][4]})

            chartData = {'packageList': packageList, 'groupsList': groupsList, 'actionLogList': actionLogList}
            returnData = {'menuList': menuListDB, 'chartData': chartData, 'Customer': Customer, 'Login_Method': Login_Method}

            request.POST = None
            request._post = None
            request._files = None

        return render(request, 'registry/registry.html', returnData)


def change_registry(request):
    arch = request.POST.get('arch')
    path = request.POST.get('path')
    name = request.POST.get('name')
    value = request.POST.get('value')
    type = request.POST.get('type')
    comName = request.POST.get('outputCGValue')
    SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    SKURL = apiUrl + SesstionKeyPath
    SKR = requests.post(SKURL, data=SKH, verify=False)
    SKRT = SKR.content.decode('utf-8', errors='ignore')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']
    PSQ = {'session': SK, 'Content-Type': 'application/json'}
    PURL = apiUrl + '/api/v2/actions'

    CURL = apiUrl + '/api/v2/groups/by-name/' + comName
    CSR = requests.get(CURL, headers=PSQ, verify=False)
    CSRT = CSR.content.decode('utf-8', errors='ignore')
    CSRJ = json.loads(CSRT)

    body = {
        "action_group": {
            "id": 4
        },
        "package_spec": {
            "source_id": 89,
            "parameters": [
                {
                    "key": "$1",
                    "value": arch,
                    "type": 1
                },
                {
                    "key": "$2",
                    "value": path,
                    "type": 1
                },
                {
                    "key": "$3",
                    "value": name,
                    "type": 1
                },
                {
                    "key": "$4",
                    "value": value,
                    "type": 1
                },
                {
                    "key": "$5",
                    "value": type,
                    "type": 1
                }
            ]
        },
        "name": "Sample Action",
        "target_group": {
            "id": CSRJ['data']['id']
        }
    }
    CA = requests.post(PURL, headers=PSQ, json=body, verify=False)
    if CA.status_code == 200:
        RGAD = DETR(CA.json(), request.user, 'registry')
        DEOP(RGAD, 'action_log')

    return redirect('deploy')


def report(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer}
    return render(request, 'common/sbom.html', returnData)

def deploy_action(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer}
    return render(request, 'deploy/deploy.html', returnData)

def deploy_action_val(request):
    #print(request.user)
    #print(request.POST.get('outputPValue'))
    if request.POST.get('outputPValue') == None or request.POST.get('outputCValue') == None or request.POST.get('outputPValue') == '' or request.POST.get('outputCValue') == '':
        pass
    else:
        packName = request.POST.get('outputPValue')
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
        CAQ = requests.post(AURL, headers=PSQ, json=body, verify=False)
        if CAQ.status_code == 200:
            DPAD = DETR(CAQ.json(), request.user)
            DEOP(DPAD, 'action_log')

        return redirect('deploy')

@csrf_exempt
def package_paging(request):
    if Customer == 'NC' or Customer == 'Xfactor':
        search = request.POST.get('search[value]')

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
        groupsList = []
        for i in range(len(dataP['data']) - 1):
            if dataP['data'][i]['content_set']['name'] == 'Default' and len(search) < 1:
                packageList.append({'id': dataP['data'][i]['id'], 'Display_name': dataP['data'][i]['display_name'], 'Content_set': dataP['data'][i]['content_set']['name'],
                                    'Command': dataP['data'][i]['command'], 'Command_Timeout': dataP['data'][i]['command_timeout']})
            elif dataP['data'][i]['content_set']['name'] == 'Default':
                if dataP['data'][i]['display_name'].startswith(search) or dataP['data'][i]['content_set']['name'].startswith(search) or dataP['data'][i]['command'].startswith(search):
                    packageList.append({'Display_name': dataP['data'][i]['display_name'], 'Content_set': dataP['data'][i]['content_set']['name'],
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
        search = request.POST.get('search[value]')

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
            if len(search) < 1:
                groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})
            else:
                if dataG['data'][i]['name'].startswith(search) or dataG['data'][i]['content_set']['name'].startswith(search) or dataG['data'][i]['text'].startswith(search):
                    groupsList.append({'Name': dataG['data'][i]['name'], 'Content_set': dataG['data'][i]['content_set']['name'], 'Expression': dataG['data'][i]['text']})

        Count = len(groupsList)
        RD = {'item': groupsList,
              'recordsTotal': Count,
              'recordsFiltered': Count,
              }
        return JsonResponse(RD)