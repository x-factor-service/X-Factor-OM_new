import requests
from django.shortcuts import render, redirect
import hashlib
import psycopg2
import json
import pandas as pd
from common.controller.controllerCommon import MenuSetting

menuListDB = MenuSetting()
def setting(request):
    with open('setting.json', 'r') as f:
        data = json.load(f)

    if request.method == 'POST':

        #----알람 수신/발신 메일----
        if request.POST.get('submit-button') == 'email-settings':
            email_id = request.POST.get('email')
            email_pw = request.POST.get('pw')

            if email_id and email_id.strip():
                data['EMAIL']['EMAIL_ID'] = email_id
            if email_pw and email_pw.strip():
                data['EMAIL']['EMAIL_PWD'] = email_pw

            to_emails = data['EMAIL']['TO_EMAIL']
            for i in range(len(to_emails)):
                field_name = 'to_email' + str(i + 1)
                email = request.POST.get(field_name, "").strip()
                if email:
                    to_emails[i] = email
                else:
                    to_emails[i] = ''

            data['EMAIL']['TO_EMAIL'] = to_emails

        #----API 접속정보----
        if request.POST.get('submit-button') == 'api-settings':
            api_url = request.POST.get('api')
            tanium_id = request.POST.get('tanium_id')
            tanium_pw = request.POST.get('tanium_pw')
            group_id = request.POST.get('group_id')
            pack_id = request.POST.get('pack_id')

            if api_url and api_url.strip():
                data['API']['apiUrl'] = api_url
            if tanium_id and tanium_id.strip():
                data['API']['username'] = tanium_id
            if tanium_pw and tanium_pw.strip():
                data['API']['password'] = tanium_pw
            if group_id and group_id.strip():
                data['API']['defaultGroupID'] = group_id
            if pack_id and pack_id.strip():
                data['API']['packageID'] = pack_id

        #----DB 접속정보----
        if request.POST.get('submit-button') == 'db-settings':
            host = request.POST.get('host')
            port = request.POST.get('port')
            db_name = request.POST.get('db_name')
            db_user = request.POST.get('db_user')
            db_pw = request.POST.get('db_pw')
            select_time = request.POST.get('select_time')

            if host and host.strip():
                data['DB']['DBHost'] = host
            if port and port.strip():
                data['DB']['DBPort'] = port
            if db_name and db_name.strip():
                data['DB']['DBName'] = db_name
            if db_user and db_user.strip():
                data['DB']['DBUser'] = db_user
            if db_pw and db_pw.strip():
                data['DB']['DBPwd'] = db_pw
            if select_time and select_time.strip():
                data['DB']['DBSelectTime'] = int(select_time)

        #----기타----
        if request.POST.get('submit-button')  == 'etc-settings':
            run_path = request.POST.get('run_path')
            if run_path and run_path.strip():
                data['FILE']['RunningService_Except']['Location'] = run_path

        with open('setting.json', 'w') as f:
            json.dump(data, f, indent=4)

        return redirect('setting')

    returnData = {'menuList': menuListDB, 'data': data}
    return render(request, 'common/setting.html', returnData)


