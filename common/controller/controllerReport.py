from django.shortcuts import render
from common.core.dashboardFunction import Dashboard
from datetime import datetime, timedelta

def report_date(request):
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        date_string = request.GET.get('date', None)
        date = datetime.strptime(date_string, '%Y-%m-%d')
        report_create_date = date.strftime('%Y-%m-%d')
        report_start_date = (date - timedelta(days=2)).strftime('%Y-%m-%d')
        report_end_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
        DCDL = Dashboard(date)
        report_listData_unMgmt_idle = DCDL["report_listData_unMgmt_idle"]
        report_listData_alarm = DCDL["report_listData_alarm"]
        report_listData_subnet_isVm = DCDL["report_listData_subnet_isVm"]
        report_listData_action_tf = DCDL["report_listData_action_tf"]
        returnData = {'report_start_date': report_start_date,
                  'report_end_date': report_end_date,
                  'report_create_date': report_create_date,
                  'report_listData_unMgmt_idle': report_listData_unMgmt_idle,
                  'report_listData_alarm': report_listData_alarm,
                  'report_listData_subnet_isVm': report_listData_subnet_isVm,
                  'report_listData_action_tf': report_listData_action_tf}
    return render(request, 'report/report_daily.html', returnData)



