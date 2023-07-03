from django.urls import path, include
from common.controller import controllerCommon, controllerDashboard, controllerMore, controllerGuide, controllerSetting

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
########################### 더보기 ##########################################
    path('certificate_more/', controllerMore.certificate_more, name='certificate_more'),
    path('certificate_more/paging/', controllerMore.certificate_more_paging, name='certificate_more_paging'),
    path('highCpuProc_more/', controllerMore.highCpuProc_more, name='highCpuProc_more'),
    path('highCpuProc_more/paging/', controllerMore.highCpuProc_more_paging, name='highCpuProc_more_paging'),
    path('setting/', controllerSetting.setting, name='setting')
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
