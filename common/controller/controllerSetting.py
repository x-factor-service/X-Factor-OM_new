import requests
from django.shortcuts import render, redirect
import hashlib
import psycopg2
import json
import pandas as pd
from common.controller.controllerCommon import MenuSetting
from django.contrib import messages

menuListDB = MenuSetting()
def setting(request):
    if request.method == 'POST':
        # 이메일과 비밀번호를 세션에 저장
        request.session['email_id'] = request.POST.get('email')
        request.session['email_pwd'] = request.POST.get('pw')

        # 여러 수신자 이메일 주소를 배열로 저장
        to_emails = []
        for i in range(1, 5):  # 이 숫자는 필드의 수에 따라 변경
            email = request.POST.get(f'to_email{i}')
            if email:  # 필드가 비어 있지 않으면 배열에 추가
                to_emails.append(email)
        request.session['to_email'] = to_emails

        # JSON 파일 열기 및 데이터 읽기
        with open('setting.json', 'r') as f:
            data = json.load(f)

        # 이메일 ID, 비밀번호 및 수신자 이메일 변경
        data['EMAIL']['EMAIL_ID'] = request.session['email_id']
        data['EMAIL']['EMAIL_PWD'] = request.session['email_pwd']
        data['EMAIL']['TO_EMAIL'] = request.session['to_email']

        # JSON 파일에 변경사항 쓰기
        with open('setting.json', 'w') as f:
            json.dump(data, f, indent=4)

        messages.success(request, '이메일과 비밀번호가 성공적으로 저장되었습니다.')
        return redirect('setting')

    returnData = {'menuList': menuListDB}
    return render(request, 'common/setting.html', returnData)

