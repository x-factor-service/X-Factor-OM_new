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

def userGuide_docs_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/documentation_ug.html', returnData)

def specification_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/specification_ug.html', returnData)

def start_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/start_ug.html', returnData)

def dashboard_public_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/dashboard_public_ug.html', returnData)

def dashboard_chart_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/dashboard_chart_ug.html', returnData)

def dashboard_etc_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/dashboard_etc_ug.html', returnData)

def weak_public_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/weak_public_ug.html', returnData)

def weak_windows_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/weak_windows_ug.html', returnData)

def weak_linux_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/weak_linux_ug.html', returnData)

def setting_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/setting_ug.html', returnData)

def report_public_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/report_public_ug.html', returnData)

def report_all_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/report_all_ug.html', returnData)

def technical_support_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/technical_support_ug.html', returnData)

def faq_ug(request):
    returnData = {'menuList': menuListDB, 'Customer': Customer,}
    return render(request, 'docs/faq_ug.html', returnData)
