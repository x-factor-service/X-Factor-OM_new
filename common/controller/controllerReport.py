from django.shortcuts import render
from common.controller.controllerCommon import MenuSetting
import json

menuListDB = MenuSetting()

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
Customer = SETTING['PROJECT']['CUSTOMER']
WorldUse = SETTING['PROJECT']['MAP']['World']
KoreaUse = SETTING['PROJECT']['MAP']['Korea']
AreaUse = SETTING['PROJECT']['MAP']['Area']['use']
AreaType = SETTING['PROJECT']['MAP']['Area']['type']
Login_Method = SETTING['PROJECT']['LOGIN']

def reportdaily(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'report/report_daily.html', returnData)