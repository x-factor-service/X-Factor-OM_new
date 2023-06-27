from django.http import JsonResponse
from django.shortcuts import render
import math
from django.views.decorators.csrf import csrf_exempt

from common.input import db as input_db

def certificate_more(request) :
    return render(request, 'common/popup/certificate_more.html')
@csrf_exempt
def certificate_more_paging(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    page = math.ceil(start / length) + 1
    data = [ str(length), str(page), str(search)]
    SMD = input_db('cert_listDataMore', data)
    SMC = input_db('cert_listDataMoreCount', data)
    RD = {"item": SMD}
    returnData = {'data': RD,
                  'draw': draw,
                  'recordsTotal': SMC,
                  'recordsFiltered': SMC,
                  }
    return JsonResponse(returnData)



