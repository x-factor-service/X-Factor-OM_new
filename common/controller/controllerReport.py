from django.shortcuts import render
from common.core.dashboardFunction import Dashboard

def report_detail(request):
    DCDL = Dashboard()
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        report_listData_unMgmt_idle = DCDL["report_listData_unMgmt_idle"]
        report_listData_alarm = DCDL["report_listData_alarm"]
        report_listData_subnet_isVm = DCDL["report_listData_subnet_isVm"]
    returnData = {'report_listData_unMgmt_idle': report_listData_unMgmt_idle,
                  'report_listData_alarm': report_listData_alarm,
                  'report_listData_subnet_isVm': report_listData_subnet_isVm}
    return render(request, 'report/report_daily.html', returnData)