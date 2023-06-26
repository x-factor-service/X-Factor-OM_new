from datetime import timedelta, datetime
from django.shortcuts import render, redirect
from om.dashboardFunctionOM import DashboardData
from common.controller.controllerCommon import MenuSetting
from om.input.db import plug_in as PDPI
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
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

def om(request):
    DCDL = DashboardData()
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        if Customer == 'NC' or Customer == 'Xfactor':
            dashboardType = 'om.html'
            MapUse = {"WorldUse": WorldUse, "KoreaUse": KoreaUse, "AreaUse": AreaUse, "AreaType": AreaType}

            # NC버전
            server_barChartData = DCDL["server_BChartDataList"]
            server_LChartDataList = DCDL["server_LChartDataList"]
            DiskChartDataList = DCDL["usageChartDataList"]["DiskChartDataList"]
            service_donutChartData = DCDL["service_donutChartData"]
            CpuChartDataList = DCDL["usageChartDataList"]["CpuChartDataList"]
            MemoryChartDataList = DCDL["usageChartDataList"]["MemoryChartDataList"]
            alamCaseDataList = DCDL["alamCaseDataList"]
            os_donutChartData = DCDL["os_donutChartData"]
            os_chartPartOne = DCDL["os_chartPartOne"]
            os_chartPartTwo = DCDL["os_chartPartTwo"]
            vendorChartList = DCDL["vendorChartList"]
            alarm_donutChartData = DCDL["alarm_donutChartData"]
            bannerData = DCDL["bannerDataList"]
            WorldMapData = DCDL["WorldMapDataList"]
            GpuServerDataList = DCDL["GpuServerDataList"]
            connectIpDataList = DCDL["connectIpDataList"]
            connectServerDataList = DCDL["connectServerDataList"]
            cpuNormalDataList = DCDL["cpuNormalDataList"]
            memoryNormalDataList = DCDL["memoryNormalDataList"]
            diskNormalDataList = DCDL["diskNormalDataList"]
            idleDataList =DCDL["idleDataList"]
            #pprint(idleDataList)
            chartData = {'DiskChartDataList': DiskChartDataList, 'donutChartDataList': service_donutChartData, 'MemoryChartDataList': MemoryChartDataList, 'CpuChartDataList': CpuChartDataList,
                        'os_donutChartData': os_donutChartData, 'server_barChartDataList': server_barChartData, "server_LChartDataList": server_LChartDataList, "alamCaseDataList": alamCaseDataList,
                        "os_chartPartOne": os_chartPartOne, "os_chartPartTwo": os_chartPartTwo, "vendorChartList": vendorChartList, "alarm_donutChartData": alarm_donutChartData,
                        "bannerDataList": bannerData, "WorldMapDataList": WorldMapData,
                        "GpuServerDataList": GpuServerDataList, "connectIpDataList": connectIpDataList, "connectServerDataList": connectServerDataList,
                        "diskNormalDataList": diskNormalDataList,
                        "memoryNormalDataList": memoryNormalDataList,
                        "cpuNormalDataList": cpuNormalDataList,
                         "idleDataList": idleDataList,
                         }


            returnData = {'menuList': menuListDB, 'chartData': chartData, 'Customer': Customer, 'MapUse': MapUse, 'Login_Method': Login_Method}
        else:
            dashboardType = 'web/dashboard.html'
            barChartData = DCDL["barChartData"]
            lineChartData = DCDL["lineChartData"]
            pieChartData = DCDL["pieChartData"]
            bannerData = DCDL["bannerData"]
            minidonutData = DCDL['MiniDonutChart']
            alarmData = DCDL["alarmListData"]
            AssociationData = DCDL["AssociationDataList"]
            WorldMapData = DCDL["WorldMapDataList"]
            TotalTopData = DCDL['TotalTopDataList']
            TotalData = DCDL["TotalDataList"]
            donutChartData = DCDL["donutChartDataList"]
            MapUse = {"WorldUse": WorldUse, "KoreaUse": KoreaUse, "AreaUse": AreaUse, "AreaType": AreaType}
            chartData = {'barChartDataList': barChartData, 'minidonutData': minidonutData, 'lineChartDataList': lineChartData, 'pieChartDataList': pieChartData, 'bannerDataList': bannerData, 'alarmDataList': alarmData, 'AssociationDataList': AssociationData,
                         'TotalTopDataList': TotalTopData, 'TotalDataList': TotalData, 'WorldMapDataList': WorldMapData, 'donutChartDataList': donutChartData}
            returnData = {'menuList': menuListDB, 'chartData': chartData, 'Customer': Customer, 'MapUse': MapUse, 'Login_Method': Login_Method}
        #print(returnData)
        return render(request, 'om.html', returnData)
def report(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'web/report.html', returnData)


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
def osVersion_moreInfo(request):
    return render(request, 'popup/osVersion_moreInfo.html')
@csrf_exempt
def osVersion_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'osMore', data)
    SMC = PDPI('statistics', 'osCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

def serverBandBy_moreInfo(request):
    return render(request, 'popup/serverBandBy_moreInfo.html')
@csrf_exempt
def serverBandBy_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'serverBandByMore', data)
    SMC = PDPI('statistics', 'serverBandByCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

def runningService_moreInfo(request):
    return render(request, 'popup/runningService_moreInfo.html')
@csrf_exempt
def runningService_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'runningServiceMore', data)
    SMC = PDPI('statistics', 'runningServiceCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

@csrf_exempt
def runningService_moreInfo_paging2(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'runningServiceMore2', data)
    SMC = PDPI('statistics', 'runningServiceCount2', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

#  IP 더보기 탭 종윤 ---------------------------------------------------------------
def connectDestinationIp_moreInfo(request):
    return render(request, 'popup/connectDestinationIp_moreInfo.html')
@csrf_exempt
def connectDestinationIp_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]


    SMD = PDPI('statistics', 'connectDestinationIpMore', data)
    for i in range(len(SMD)):
        ip = SMD[i]['ip']
        SMD[i]['ip'] = ip.split(':')[0]
        SMD[i]['port'] = ip.split(':')[1]

    SMC = PDPI('statistics', 'connectDestinationIpCount', data)

    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

def connectSourceIp_moreInfo(request):
    return render(request, 'popup/connectSourceIp_moreInfo.html')
@csrf_exempt
def connectSourceIp_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]

    SMD = PDPI('statistics', 'connectSourceIpMore', data)
    SMC = PDPI('statistics', 'connectSourceIpCount', data)

    RD = {"item": SMD}

    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)
# ---------------------------------------------------------------------------------

def memory_moreInfo(request):
    # memoryMoreDataList = DCDL["memoryMoreDataList"]
    # chartData = {"memoryMoreDataList": memoryMoreDataList}
    # returnData = {'menuList': menuListDB, "chartData": chartData}
    return render(request, 'popup/memory_moreInfo.html')

@csrf_exempt
def memory_moreInfo_paging(request):

    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'memoryMore', data)
    SMC = PDPI('statistics', 'memoryCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

def cpu_moreInfo(request):
    return render(request, 'popup/cpu_moreInfo.html')

@csrf_exempt
def cpu_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'cpuMore', data)
    SMC = PDPI('statistics', 'cpuCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

def disk_moreInfo(request):
    return render(request, 'popup/disk_moreInfo.html')
@csrf_exempt
def disk_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'diskMore', data)
    SMC = PDPI('statistics', 'diskCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

def physicalServer_moreInfo(request):
    return render(request, 'popup/physicalServer_moreInfo.html')
@csrf_exempt
def physicalServer_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'physicalServerMore', data)
    SMC = PDPI('statistics', 'physicalServerCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

def gpuServer_moreInfo(request):
    return render(request, 'popup/gpuServer_moreInfo.html')
@csrf_exempt
def gpuServer_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'gpuServerMore', data)
    for i in range(len(SMD)):
        model = SMD[i]['model']
        SMD[i]['model'] = model.split(',')[1].replace('}', '').replace('"','')
        SMD[i]['count'] = str(list(model)[1])

    # for i in range(len(SMD)):
    #     model = eval(SMD[i]['model'])
    #     if type(list(model)[0]) == str:
    #         SMD[i]['model'] = list(model)[0]
    #         SMD[i]['count'] = str(list(model)[1])
    #     else:
    #         SMD[i]['model'] = list(model)[1]
    #         SMD[i]['count'] = str(list(model)[0])

        # model = SMD[i]['model'].replace(',', '').replace('"', '').replace('{', '').replace('}','')[1:]
        # count = SMD[i]['model'].replace(',', '').replace('"', '').replace('{', '').replace('}','')[0]
        # SMD[i] = {"count": count}
    SMC = PDPI('statistics', 'gpuServerCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

def alarmCase_moreInfo(request):
    return render(request, 'popup/alarmCase_moreInfo.html')
@csrf_exempt
def alarmCase_moreInfo_paging(request):
    halfHour = (datetime.now() - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
    halfHour = datetime.strptime(halfHour, "%Y-%m-%d %H:%M:%S")
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = PDPI('statistics', 'alarmCaseMore', data)
    for i in range(len(SMD)):
        if SMD[i]['date'] == 'True':
            if SMD[i]['ramusage'] > 95:
                SMD[i]['ramusage'] = 'True (' + str(SMD[i]['ramusage']) + ')'
            elif SMD[i]['ramusage'] == -1:
                SMD[i]['ramusage'] = 'unconfirmed'
            else:
                SMD[i]['ramusage'] = 'False'

            if SMD[i]['cpuusage'] > 95:
                SMD[i]['cpuusage'] = 'True (' + str(SMD[i]['cpuusage']) + ')'
            elif SMD[i]['cpuusage'] == -1:
                SMD[i]['cpuusage'] = 'unconfirmed'
            else:
                SMD[i]['cpuusage'] = 'False'

            if SMD[i]['driveusage'] > 95:
                SMD[i]['driveusage'] = 'True (' + str(SMD[i]['driveusage']) + ')'
            elif SMD[i]['driveusage'] == -1:
                SMD[i]['driveusage'] = 'unconfirmed'
            else:
                SMD[i]['driveusage'] = 'False'
        else:
            if SMD[i]['ramusage'] > 95:
                SMD[i]['ramusage'] = 'True (' + str(SMD[i]['ramusage']) + ')'
                if SMD[i]['cpuusage'] > 95:
                    SMD[i]['cpuusage'] = 'True (' + str(SMD[i]['cpuusage']) + ')'
                elif SMD[i]['cpuusage'] == -1:
                    SMD[i]['cpuusage'] = 'unconfirmed'
                else:
                    SMD[i]['cpuusage'] = 'False'

                if SMD[i]['driveusage'] > 95:
                    SMD[i]['driveusage'] = 'True (' + str(SMD[i]['driveusage']) + ')'
                elif SMD[i]['driveusage'] == -1:
                    SMD[i]['driveusage'] = 'unconfirmed'
                else:
                    SMD[i]['driveusage'] = 'False'

            elif SMD[i]['cpuusage'] > 95:
                SMD[i]['cpuusage'] = 'True (' + str(SMD[i]['cpuusage']) + ')'
                if SMD[i]['ramusage'] > 95:
                    SMD[i]['ramusage'] = 'True (' + str(SMD[i]['ramusage']) + ')'
                elif SMD[i]['ramusage'] == -1:
                    SMD[i]['ramusage'] = 'unconfirmed'
                else:
                    SMD[i]['ramusage'] = 'False'

                if SMD[i]['driveusage'] > 95:
                    SMD[i]['driveusage'] = 'True (' + str(SMD[i]['driveusage']) + ')'
                elif SMD[i]['driveusage'] == -1:
                    SMD[i]['driveusage'] = 'unconfirmed'
                else:
                    SMD[i]['driveusage'] = 'False'

            elif SMD[i]['driveusage'] > 95:
                SMD[i]['driveusage'] = 'True (' + str(SMD[i]['driveusage']) + ')'
                if SMD[i]['ramusage'] > 95:
                    SMD[i]['ramusage'] = 'True (' + str(SMD[i]['ramusage']) + ')'
                elif SMD[i]['ramusage'] == -1:
                    SMD[i]['ramusage'] = 'unconfirmed'
                else:
                    SMD[i]['ramusage'] = 'False'

                if SMD[i]['cpuusage'] > 95:
                    SMD[i]['cpuusage'] = 'True (' + str(SMD[i]['driveusage']) + ')'
                elif SMD[i]['cpuusage'] == -1:
                    SMD[i]['cpuusage'] = 'unconfirmed'
                else:
                    SMD[i]['cpuusage'] = 'False'


    SMC = PDPI('statistics', 'alarmCaseCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)

@csrf_exempt
def send_email_view(request):
    if request.method == "POST":
        subject = "알람"
        ip = request.POST['ip']
        name = request.POST['name']
        ram = request.POST['ram']
        cpu = request.POST['cpu']
        drive = request.POST['drive']
        date = request.POST['date']

        body = ip + ' ip를 사용하는 컴퓨터가 경고가 발생하였습니다. \n' + name + ' 컴퓨터를 체크해주시길 바랍니다.'
        to_email = "djlee@xionits.com"

        msg = MIMEMultipart()
        msg['From'] = Email_id
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()
            server.login(Email_id, Email_pwd)
            text = msg.as_string()
            server.sendmail(Email_id, to_email, text)
            server.quit()
            print('이메일이 성공적으로 전송되었습니다.')
        except Exception as e:
            print(f'이메일 전송 중 오류 발생: {e}')
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail'})


@csrf_exempt
def send_reboot_view(request):
    if request.method == "POST":
        try:
            subject = "reboot"
            # name = request.POST['name']
            print(request.POST['name'])
            name = 'jh-test'
            ###################### 세션키 받기 ##################
            SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
            SKURL = apiUrl + SesstionKeyPath
            SKR = requests.post(SKURL, data=SKH, verify=False)
            SKRT = SKR.content.decode('utf-8')
            SKRJ = json.loads(SKRT)
            SK = SKRJ['data']['session']
            print("SessionKey 불러오기 성공")

            ################ Computer Group 만들기 ###################
            CCGH = {'session': SK, 'Content-Type': 'text/plain'}
            CCGURL = apiUrl + '/api/v2/groups'
            CCGB = '{"name" : "' + subject + name + '","text" : "Computer Name matches ' + name + '"}'
            CCG = requests.post(CCGURL, headers=CCGH, data=CCGB, verify=False)
            CGID = str(CCG.json()['data']['id'])
            print("Computer Group 만들기 성공")

            ################## actrion 만들기 ##########################
            CAH = {'session': SK, 'Content-Type': 'text/plain'}
            CAURL = apiUrl + '/api/v2/actions'
            CAB = '{"name": "reboot test","action_group": {"id": ' + DEFAULTGROUPID + '},"package_spec": {"source_id": ' + PACKAGEID + '},"target_group": {"id": ' + CGID + '}}'
            CA = requests.post(CAURL, headers=CAH, data=CAB, verify=False)
            sleep(5)
            print("Action 성공")

            ################### action 성공시 Delete Computer Group #############################
            if CA.status_code == 200:
                DCGH = {'session': SK, 'Content-Type': 'text/plain'}
                DCGURL = apiUrl + '/api/v2/groups/' + CGID
                DCG = requests.delete(DCGURL, headers=DCGH, verify=False)
                if DCG.status_code == 200:
                    print("Computer Group 지우기 성공")
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'fail'})
            else:
                return JsonResponse({'status': 'fail'})
        except Exception as e:
            print(f'Reboot 기능 오류 발생: {e}')