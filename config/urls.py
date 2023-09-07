from django.urls import path, include
from common.controller import controllerCommon, controllerDashboard, controllerMore, controllerGuide, controllerSetting, controllerReport
from deploy import controllerDeploy
from registry import controllerRegistry
from sbom import controllerSBOM
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', controllerCommon.login, name=''),
    path('login/', controllerCommon.login, name='login'),
    path('signup/', controllerCommon.signup, name='signup'),
    path('logout/', controllerCommon.logout, name='logout/'),
    path('updateform/', controllerCommon.updateform, name='updateform'),
    path('update/', controllerCommon.update, name='update'),
    path('dashboard/', controllerDashboard.dashboard, name='dashboard'),
########################### 유저 가이드 ##########################################
    path('documentation_ug/', controllerGuide.userGuide_docs_ug, name='userGuide_docs_ug'),
    path('specification_ug/', controllerGuide.specification_ug, name='specification_ug'),
    path('start_ug/', controllerGuide.start_ug, name='start_ug'),
    path('dashboard_public_ug/', controllerGuide.dashboard_public_ug, name='dashboard_public_ug'),
    path('dashboard_chart_ug/', controllerGuide.dashboard_chart_ug, name='dashboard_chart_ug'),
    path('dashboard_etc_ug/', controllerGuide.dashboard_etc_ug, name='dashboard_etc_ug'),
    path('weak_public_ug/', controllerGuide.weak_public_ug, name='weak_public_ug'),
    path('weak_windows_ug/', controllerGuide.weak_windows_ug, name='weak_windows_ug'),
    path('weak_linux_ug/', controllerGuide.weak_linux_ug, name='weak_linux_ug'),
    path('setting_ug/', controllerGuide.setting_ug, name='setting_ug'),
    path('report_public_ug/', controllerGuide.report_public_ug, name='report_public_ug'),
    path('report_all_ug/', controllerGuide.report_all_ug, name='report_all_ug'),
    path('technical_support_ug/', controllerGuide.technical_support_ug, name='technical_support_ug'),
    path('faq_ug/', controllerGuide.faq_ug, name='faq_ug'),
    path('sbom/', controllerSBOM.sbom, name='sbom'),
    path('sbom/paging/', controllerSBOM.sbom_paging, name='sbom_paging'),
    path('sbom/paging_cve/', controllerSBOM.sbom_cve_paging, name='sbom_cve_paging'),
    path('sbom/paging_sic/', controllerSBOM.sbom_in_cve, name='sbom_in_cve'),
    path('sbom/paging_cis/', controllerSBOM.cve_in_sbom, name='cve_in_sbom'),
    path('sbom_detail/', controllerSBOM.sbom_detail, name='sbom_detail'),
    path('sbom/cve_detail/', controllerSBOM.cve_detail, name='cve_detail'),
    path('deploy/', controllerDeploy.deploy, name='deploy'),
    path('deploy/package/', controllerDeploy.package_paging, name='package_paging'),
    path('deploy/computerGroup/', controllerDeploy.computerGroup_paging, name='computerGroup_paging'),
    path('deploy_action_val/', controllerDeploy.deploy_action_val, name='deploy_action_val'),
    path('deploy/packCheck/', controllerDeploy.packCheck, name='packCheck'),
    path('registry/', controllerRegistry.registry, name='registry'),
    path('change_registry/', controllerRegistry.change_registry, name='change_registry'),
    # path('certificate_more/', controllerMore.certificate_more, name='certificate_more'),
    # path('certificate_more/paging/', controllerMore.certificate_more_paging, name='certificate_more_paging'),
    path('highCpuProc_more/', controllerMore.highCpuProc_more, name='highCpuProc_more'),
    path('highCpuProc_more/paging/', controllerMore.highCpuProc_more_paging, name='highCpuProc_more_paging'),
    path('highMemProc_more/', controllerMore.highMemProc_more, name='highMemProc_more'),
    path('highMemProc_more/paging/', controllerMore.highMemProc_more_paging, name='highMemProc_more_paging'),
    path('highDiskApp_more/', controllerMore.highDiskApp_more, name='highDiskApp_more'),
    path('highDiskApp_more/paging/', controllerMore.highDiskApp_more_paging, name='highDiskApp_more_paging'),
    path('setting/', controllerSetting.setting, name='setting'),
    path('setting/running_setting/', controllerSetting.running_setting, name='running_setting'),
    path('setting/delete_running_service/', controllerSetting.delete_running_service, name='delete_running_service'),

########################## 리포트 ###########################################
    path('report_date/', controllerReport.report_date, name='report_date'),
]
# path('admin/', admin.site.urls),
# path('om/', include(om.urls), name="om"),
# path('cspm/', include(cspm.urls), name="cspm"),
# path('sm/', include(sm.urls), name="sm"),
# path('asset/', base_views.assetweb, name='asset'),
# path('asset_detail/', base_views.assetDetailweb, name='asset_detail'),
# path('asset_detail/paging', base_views.assetDetailweb_paging, name='asset_detail_paging'),
# path('report/', base_views.report, name='report'),
# path('dashboard/', base_views.dashboard, name='dashboard'),
# path('reportdaily/', base_views.reportdaily, name='reportdaily'),
# path('reportmonthly/', base_views.reportmonthly, name='reportmonthly'),
# path('send_email/', controller.send_email_view, name='send_email'),
# path('send_reboot/', controller.send_reboot_view, name='send_reboot'),

####### om URL 파일 호출 ##########
try:
    import om.urls
    urlpatterns.append(path('om/', include(om.urls), name="om"))
except (ImportError):
    pass

####### cspm URL 파일 호출 ##########
try:
    import cspm.urls
    urlpatterns.append(path('cspm/', include(cspm.urls), name="cspm"))
except (ImportError):
    pass

####### sm URL 파일 호출 ##########
try:
    import sm.urls
    urlpatterns.append(path('sm/', include(sm.urls), name="sm"))
except (ImportError):
    pass
