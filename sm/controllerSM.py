from django.shortcuts import render

def index(request):
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'om/login.html', res_data)
    else:
        dashboard = 'om/dashboard.html'
        MapUse = {"WorldUse": WorldUse, "KoreaUse": KoreaUse, "AreaUse": AreaUse, "AreaType": AreaType}
##
        ResourceDiskChartDataList = DCDL["ResourceDiskChartDataList"]
        ResourceMemoryChartDataList= DCDL["ResourceMemoryChartDataList"]
##
        vendorChartList = DCDL["vendorChartList"]
        alarm_donutChartData = DCDL["alarm_donutChartData"]

        GpuServerDataList = DCDL["GpuServerDataList"]

        wire_pieChartData = DCDL["wire_pieChartData"]
        os_pieChartData = DCDL["os_pieChartData"]
        virtual_pieChartData = DCDL["virtual_pieChartData"]
        chartData = {'DiskChartDataList': DiskChartDataList, 'donutChartDataList': service_donutChartData, 'MemoryChartDataList': MemoryChartDataList, 'CpuChartDataList': CpuChartDataList,
                    "server_LChartDataList": server_LChartDataList,
                    "ResourceDiskChartDataList": ResourceDiskChartDataList,
                    "ResourceMemoryChartDataList": ResourceMemoryChartDataList,
                    "vendorChartList": vendorChartList,
                    "alarm_donutChartData": alarm_donutChartData,
#                        "bannerDataList": bannerData,
                    "GpuServerDataList": GpuServerDataList,
                    "wire_pieChartData": wire_pieChartData,
                    "os_pieChartData": os_pieChartData,
                    "virtual_pieChartData": virtual_pieChartData
                     }

        returnData = {'menuList': menuListDB, 'chartData': chartData, 'Customer': Customer, 'MapUse': MapUse, 'Login_Method': Login_Method}

        return render(request, dashboardType, returnData)