from django.shortcuts import render
from common.controller.controllerCommon import MenuSetting

menuListDB = MenuSetting()

def reg_setting(request):
    res_data = {}
    if not 'sessionid' in request.session:
        res_data['error'] = '먼저 로그인을 해주세요.'
        return render(request, 'common/login.html', res_data)
    else:
        returnData = {'menuList': menuListDB}
        return render(request, 'common/regSetting.html', returnData)



