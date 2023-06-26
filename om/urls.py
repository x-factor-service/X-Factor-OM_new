from django.urls import path
from om import controllerOM

urlpatterns = [
    path('', controllerOM.om , name='om'),
    path('osVersion_moreInfo/', controllerOM.osVersion_moreInfo, name='osVersion_moreInfo'),
    path('osVersion_moreInfo/paging/', controllerOM.osVersion_moreInfo_paging, name='osVersion_moreInfo_paging'),
    path('serverBandBy_moreInfo/', controllerOM.serverBandBy_moreInfo, name='serverBandBy_moreInfo'),
    path('serverBandBy_moreInfo/paging/', controllerOM.serverBandBy_moreInfo_paging, name='serverBandBy_moreInfo_paging'),
    path('runningService_moreInfo/', controllerOM.runningService_moreInfo, name='runningService_moreInfo'),
    path('runningService_moreInfo/paging/', controllerOM.runningService_moreInfo_paging, name='runningService_moreInfo_paging'),
    path('runningService_moreInfo/paging2/', controllerOM.runningService_moreInfo_paging2, name='runningService_moreInfo_paging2'),
    path('memory_moreInfo/', controllerOM.memory_moreInfo, name='memory_moreInfo'),
    path('memory_moreInfo/paging/', controllerOM.memory_moreInfo_paging, name='memory_moreInfo_paging'),
    path('cpu_moreInfo/', controllerOM.cpu_moreInfo, name='cpu_moreInfo'),
    path('cpu_moreInfo/paging/', controllerOM.cpu_moreInfo_paging, name='cpu_moreInfo_paging'),
    path('disk_moreInfo/', controllerOM.disk_moreInfo, name='disk_moreInfo'),
    path('disk_moreInfo/paging/', controllerOM.disk_moreInfo_paging, name='disk_moreInfo_paging'),
    path('physicalServer_moreInfo/', controllerOM.physicalServer_moreInfo, name='physicalServer_moreInfo'),
    path('physicalServer_moreInfo/paging/', controllerOM.physicalServer_moreInfo_paging, name='physicalServer_moreInfo_paging'),
    path('gpuServer_moreInfo/', controllerOM.gpuServer_moreInfo, name='gpuServer_moreInfo'),
    path('gpuServer_moreInfo/paging/', controllerOM.gpuServer_moreInfo_paging, name='gpuServer_moreInfo_paging'),
    path('alarmCase_moreInfo/', controllerOM.alarmCase_moreInfo, name='alarmCase_moreInfo'),
    path('alarmCase_moreInfo/paging/', controllerOM.alarmCase_moreInfo_paging, name='alarmCase_moreInfo_paging'),
    path('send_email/', controllerOM.send_email_view, name='send_email'),
    path('send_reboot/', controllerOM.send_reboot_view, name='send_reboot'),
]