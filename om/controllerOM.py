from datetime import timedelta, datetime
import psycopg2
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
DBHost = SETTING['DB']['DBHost']
DBPort = SETTING['DB']['DBPort']
DBName = SETTING['DB']['DBName']
DBUser = SETTING['DB']['DBUser']
DBPwd = SETTING['DB']['DBPwd']

menuListDB = MenuSetting()

def omsql():
    Conn = psycopg2.connect(
        'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
    Cur = Conn.cursor()
    query = """
                SELECT os_chartPartOne, os_chartPartTwo, os_donutChartData, idleDataList, server_BChartDataList, service_donutChartData, DiskChartDataList, CpuChartDataList, MemoryChartDataList, diskNormalDataList, cpuNormalDataList, memoryNormalDataList, server_LChartDataList, WorldMapDataList, alamCaseDataList, alarm_donutChartData, vendorChartList, connectIpDataList, connectServerDataList, bannerData, om_collection_date
FROM om 
ORDER BY om_collection_date DESC
LIMIT 1;
                    """
    Cur.execute(query)
    RS = Cur.fetchall()
    return RS

def om(request):
    o = omsql()
    # DCDL = DashboardData()
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        if Customer == 'NC' or Customer == 'Xfactor':
            dashboardType = 'om.html'
            MapUse = {"WorldUse": WorldUse, "KoreaUse": KoreaUse, "AreaUse": AreaUse, "AreaType": AreaType}


            os_chartPartOne = eval(o[0][0])
            os_chartPartTwo = eval(o[0][1])
            os_donutChartData = eval(o[0][2])
            idleDataList = eval(o[0][3])
            server_barChartData = eval(o[0][4])
            service_donutChartData = eval(o[0][5])
            DiskChartDataList = eval(o[0][6])
            CpuChartDataList = eval(o[0][7])
            MemoryChartDataList = eval(o[0][8])
            diskNormalDataList = o[0][9]
            cpuNormalDataList = o[0][10]
            memoryNormalDataList = o[0][11]
            server_LChartDataList = eval(o[0][12])
            WorldMapData = eval(o[0][13])
            alamCaseDataList = eval(o[0][14])
            alarm_donutChartData = eval(o[0][15])
            vendorChartList = eval(o[0][16])
            connectIpDataList = eval(o[0][17])
            connectServerDataList = eval(o[0][18])
            bannerData = eval(o[0][19])
            om_collection_date = o[0][20]

            #pprint(idleDataList)
            chartData = {'DiskChartDataList': DiskChartDataList, 'donutChartDataList': service_donutChartData, 'MemoryChartDataList': MemoryChartDataList, 'CpuChartDataList': CpuChartDataList,
                        'os_donutChartData': os_donutChartData, 'server_barChartDataList': server_barChartData, "server_LChartDataList": server_LChartDataList, "alamCaseDataList": alamCaseDataList,
                        "os_chartPartOne": os_chartPartOne, "os_chartPartTwo": os_chartPartTwo, "vendorChartList": vendorChartList, "alarm_donutChartData": alarm_donutChartData,
                        "bannerDataList": bannerData, "WorldMapDataList": WorldMapData,
                        "connectIpDataList": connectIpDataList, "connectServerDataList": connectServerDataList,
                        "diskNormalDataList": diskNormalDataList,
                        "memoryNormalDataList": memoryNormalDataList,
                        "cpuNormalDataList": cpuNormalDataList,
                         "idleDataList": idleDataList,
                         }


            returnData = {'menuList': menuListDB, 'chartData': chartData, 'Customer': Customer, 'MapUse': MapUse, 'Login_Method': Login_Method, 'om_collection_date':om_collection_date}
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



def idle_moreInfo(request):
    return render(request, 'popup/idle_moreInfo.html')

@csrf_exempt
def idle_moreInfo_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    IDM = PDPI('statistics', 'idleMore', data)

    IDC = PDPI('statistics', 'idleMoreCount', data)
    RD = {"item": IDM}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': IDC,
                  'recordsFiltered': IDC,
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

        items = []
        if 'True' in ram:
            items.append('메모리 사용량 95% 초과')
        if 'True' in cpu:
            items.append('CPU 사용량 95% 초과')
        if 'True' in drive:
            items.append('디스크 사용량 99% 초과')
        if 'True' in date:
            items.append('최근 30분 이내 오프라인 여부')

        body = ip + ' ip를 사용하는 컴퓨터가 경고가 발생하였습니다. \n' + name + ' 컴퓨터를 체크해주시길 바랍니다.'

        # JSON 파일에서 이메일 ID, 비밀번호 및 수신자 이메일 목록 읽기
        with open('setting.json', 'r') as f:
            data = json.load(f)
        Email_id = data['EMAIL']['EMAIL_ID']
        Email_pwd = data['EMAIL']['EMAIL_PWD']
        to_emails = data['EMAIL']['TO_EMAIL']  # 이제 'to_email' 변수는 배열

        msg = MIMEMultipart()
        msg['From'] = Email_id
        msg['To'] = ', '.join(to_emails)  # 이메일 헤더에는 쉼표로 구분된 문자열이 필요합니다
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP('smtp.office365.com', 587)
            server.starttls()
            server.login(Email_id, Email_pwd)
            print(server.login(Email_id, Email_pwd))
            text = msg.as_string()
            server.sendmail(Email_id, to_emails, text)  # 여기서 'to_emails'는 배열
            server.quit()
            print('이메일이 성공적으로 전송되었습니다.')

            # ------------------------------OM 리포트 알람 -------------------------------
            conn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
            cur = conn.cursor()
            current_time = datetime.now()
            cur.execute("SELECT COUNT(*) FROM report_statistics WHERE statistics_collection_date::date = %s", (current_time.date(),))
            count = cur.fetchone()[0]
            if count == 0:
                for item in items:
                    cur.execute("INSERT INTO report_statistics (classification, item, package_name, target, item_count, statistics_collection_date) VALUES (%s, %s, %s, %s, %s, %s)", ('daily_om_alarm', item, None, None, 1, current_time))
            else:
                for item in items:
                    cur.execute(
                        "SELECT item FROM report_statistics WHERE statistics_collection_date::date = %s AND item = %s",
                        (current_time.date(), item))
                    result = cur.fetchone()
                    if result:
                        cur.execute(
                            "UPDATE report_statistics SET item_count = item_count::integer + 1, statistics_collection_date = %s WHERE statistics_collection_date::date = %s AND item = %s",
                            (current_time, current_time.date(), item))
                    else:
                        cur.execute(
                            "INSERT INTO report_statistics (classification, item, package_name, target, item_count, statistics_collection_date) VALUES (%s, %s, %s, %s, %s, %s)",
                            ('daily_om_alarm', item, None, None, 1, current_time))
            conn.commit()
            cur.close()
            conn.close()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f'이메일 전송 중 오류 발생: {e}')
            return JsonResponse({'status': 'error'})
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
            SKRT = SKR.content.decode('utf-8', errors='ignore')
            SKRJ = json.loads(SKRT)
            SK = SKRJ['data']['session']
            #print("SessionKey 불러오기 성공")

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



@csrf_exempt
def send_off_process_view(request):
    if request.method == "POST":
        try:
            subject = "off_process"
            name = request.POST['name']
            IM = request.POST['IM']
            value = request.POST['value']
            os = request.POST['os']
            # 세션키 받기
            SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
            SKURL = apiUrl + SesstionKeyPath
            SKR = requests.post(SKURL, data=SKH, verify=False)
            SKRT = SKR.content.decode('utf-8', errors='ignore')
            SKRJ = json.loads(SKRT)
            SK = SKRJ['data']['session']
            #print("SessionKey 불러오기 성공")

            # Computer Group 만들기
            CCGH = {'session': SK, 'Content-Type': 'text/plain'}
            CCGURL = apiUrl + '/api/v2/groups'
            CCGB = '{"name" : "' + subject + name + '","text" : "Computer Name matches ' + name + '"}'
            CCG = requests.post(CCGURL, headers=CCGH, data=CCGB, verify=False)
            CGID = str(CCG.json()['data']['id'])
            print("Computer Group 만들기 성공")

            # package 만들기
            CPH = {'session': SK, 'Content-Type': 'text/plain'}
            CPHURL = apiUrl + '/api/v2/packages/'
            if os == "Windows":
                CPB = '{"name" : "' + subject + name + '", "command" : "cmd /d /c taskkill /f /IM ' + IM + '.exe"}'
            elif os == "Linux":
                CPB = '{"name" : "' + subject + name + '", "command" : "/bin/bash killall -9 ' + IM + '"}'
            CP = requests.post(CPHURL, headers=CPH, data=CPB, verify=False)
            CPID = str(CP.json()['data']['id'])
            print("package 만들기 성공")

            # action 만들기
            CAH = {'session': SK, 'Content-Type': 'text/plain'}
            CAURL = apiUrl + '/api/v2/actions'
            CAB = '{"name": "package_test3","action_group": {"id": ' + DEFAULTGROUPID + '},"package_spec": {"source_id": ' + CPID + '},"target_group": {"id": ' + CGID + '}}'
            CA = requests.post(CAURL, headers=CAH, data=CAB, verify=False)
            sleep(5)
            print("Action 성공")

            # 패키지 지우기

            DPH = {'session': SK, 'Content-Type': 'text/plain'}
            DPURL = apiUrl + '/api/v2/packages/' + CPID
            DP = requests.delete(DPURL, headers=DPH, verify=False)

            if DP.status_code == 200:
                print("Package 지우기 성공")
                sleep(5)

            # 성공시 computer group 지우기
            if CA.status_code == 200:
                DCGH = {'session': SK, 'Content-Type': 'text/plain'}
                DCGURL = apiUrl + '/api/v2/groups/' + CGID
                DCG = requests.delete(DCGURL, headers=DCGH, verify=False)

                if DCG.status_code == 200:
                    print("Computer Group 지우기 성공")
                    sleep(5)
                    return JsonResponse({'status': 'success'})
                else:
                    return JsonResponse({'status': 'fail'})

            else:
                return JsonResponse({'status': 'fail'})

        except Exception as e:
            print(f'off_process 기능 오류 발생: {e}')