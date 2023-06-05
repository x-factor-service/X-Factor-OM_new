import requests
from django.shortcuts import render, redirect
import hashlib
import psycopg2
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from time import sleep

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
APIUNM = SETTING['API']['username']
APIPWD = SETTING['API']['password']
DEFAULTGROUPID = SETTING['API']['defaultGroupID']
PACKAGEID = SETTING['API']['packageID']
Email_id = SETTING['EMAIL']['EMAIL_ID']
Email_pwd = SETTING['EMAIL']['EMAIL_PWD']

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