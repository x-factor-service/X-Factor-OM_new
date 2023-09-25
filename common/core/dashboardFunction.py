import logging
from common.input.db import plug_in as inputDb
from common.core.transform import plug_in as reportTf, plug_in_action as report_actionTf, plug_in_number as numberTf
import urllib3
import json

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
core = SETTING['PROJECT']['CORE']
ProjectType = SETTING['PROJECT']['TYPE']
Customer = SETTING['PROJECT']['CUSTOMER']

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#####################################  메인 대시보드 페이지  ################################################
def Dashboard(type=None):
    logger = logging.getLogger(__name__)
    if Customer == 'NC' or Customer == 'Xfactor':
        disk_donutData = []
        memory_donutData = []
        cpu_donutData = []
        wire_pieData = []
        os_pieData = []
        virtual_pieData = []
        discover_lineData = []
        allAsset_lineData = []
        # cert_listData = []
        sbom_listData = []
        idle_lineData = []
        highCpuProc_listData = []
        highMemProc_listData = []
        highDiskApp_listData = []
        report_listData_unMgmt_idle = []
        report_listData_alarm = []
        report_listData_subnet_isVm_tf = []
        report_listData_action_tf = []
        allOnline_donutData = []
        deployToday_barData = []


            #------------------------------상단 디스크 사용률 도넛 차트------------------------
        try:
            disk_donutData_input = inputDb('disk_donutData')
            disk_donutData = numberTf(disk_donutData_input)
            logger.info('dashboardFunction.py - disk_donutData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - disk_donutData')

            # -----------------------------상단 메모리 사용률 도넛 차트------------------------------
        try:
            memory_donutData_input = inputDb('memory_donutData')
            memory_donutData = numberTf(memory_donutData_input)
            logger.info('dashboardFunction.py - memory_donutData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - memory_donutData')
            # -----------------------------상단 씨피유 사용률 도넛 차트------------------------------
        try:
            cpu_donutData_input = inputDb('cpu_donutData')
            cpu_donutData = numberTf(cpu_donutData_input)
            logger.info('dashboardFunction.py - cpu_donutData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - cpu_donutData')
            # -----------------------------상단 오에스 파이차트 ------------------------------------
        try:
            os_pieData = inputDb('os_pieData')
            logger.info('dashboardFunction.py - os_pieData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - os_pieData')
            # -----------------------------상단 유/무선(와이어) 파이차트 ------------------------------------
        try:
            wire_pieData = inputDb('wire_pieData')
            logger.info('dashboardFunction.py - wire_pieData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - wire_pieData')
            # -----------------------------상단 물리/가상 파이차트 ------------------------------------
        try:
            virtual_pieData = inputDb('virtual_pieData')
            logger.info('dashboardFunction.py - virtual_pieData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - virtual_pieData')
            # -----------------------------중앙 관리자산 라인차트 ------------------------------------
        try:
            allAsset_lineData = inputDb('allAsset_lineData')
            logger.info('dashboardFunction.py - allAsset_lineData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - allAsset_lineData')
            # -----------------------------중앙 미관리자산 라인차트 ------------------------------------
        try:
            discover_lineData = inputDb('discover_lineData')
            logger.info('dashboardFunction.py - discover_lineData - Success')
            #print(discover_lineData)
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - discover_lineData')
            # -----------------------------중앙 유휴자산 라인차트 ------------------------------------
        try:
            idle_lineData = inputDb('idle_lineData')
            logger.info('dashboardFunction.py - idle_lineData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - idle_lineData')
        # -----------------------------인증서리스트  ------------------------------------
        # try:
        #     cert_listData = inputDb('cert_listData')
        #     logger.info('dashboardFunction.py - cert_listData - Success')
        # except:
        #     logger.debug('dashboardFunction.py - Error Occurred')
        #     logger.debug('Error - cert_listData')
        # -----------------------------최대 CPU 점유 프로세스 더보기 -----------------------
        try:
            highCpuProc_listData = inputDb('highCpuProc_listData')
            logger.info('dashboardFunction.py - highCpuProc_listData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - highCpuProc_listData')
        # -----------------------------최대 MEMORY 점유 프로세스 더보기 -----------------------
        try:
            highMemProc_listData = inputDb('highMemProc_listData')
            logger.info('dashboardFunction.py - highMemProc_listData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - highMemProc_listData')
        # -----------------------------최대 DISK 점유 어플리케이션 더보기 -----------------------
        try:
            highDiskApp_listData = inputDb('highDiskApp_listData')
            logger.info('dashboardFunction.py - highDiskApp_listData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - highDiskApp_listData')
        # ---------------------------------OM 일일 리포트 - 자산 통계 정보 ---------------------
        try:
            report_listData_unMgmt_idle = inputDb('report_listData_unMgmt_idle', type)
            logger.info('dashboardFunction.py - report_listData_unMgmt_idle - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - report_listData_unMgmt_idle')
        # ---------------------------------OM 일일 리포트 - 전일 발송된 알람 정보 ---------------
        try:
            report_listData_alarm = inputDb('report_listData_alarm', type)
            logger.info('dashboardFunction.py - report_listData_alarm - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - report_listData_alarm')
        # ---------------------------------OM 일일 리포트 - IP대역별 관리 자산 현황
        try:
            report_listData_subnet_isVm = inputDb('report_listData_subnet_isVm', type)
            report_listData_subnet_isVm_tf = reportTf(report_listData_subnet_isVm)
            logger.info('dashboardFunction.py - report_listData_alarm - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - report_listData_subnet_isVm_tf')
        # ---------------------------------OM 일일 리포트 - 배포 성공한 Package
        try:
            report_listData_action = inputDb('report_listData_action', type)
            report_listData_action_tf = report_actionTf(report_listData_action)
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - report_listData_action')
        # ---------------------------------온라인 상태 전체 자산 수
        try:
            allOnline_donutData_input = inputDb('allOnline_donutData')
            allOnline_donutData = numberTf(allOnline_donutData_input)
            logger.info('dashboardFunction.py - allOnline_donutData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - allOnline_donutData')
        # ------------------금일 가장 많이 배포한 패키지 Top 5 -------------------
        try:
            deployToday_barData = inputDb('deployToday_barData')
            logger.info('dashboardFunction.py - deployToday_barData - Success')
        except:
            logger.debug('dashboardFunction.py - Error Occurred')
            logger.debug('Error - deployToday_barData')

        RD = {
            'disk_donutData': disk_donutData,
            'memory_donutData': memory_donutData,
            'cpu_donutData': cpu_donutData,
            'wire_pieData': wire_pieData,
            "os_pieData": os_pieData,
            "virtual_pieData": virtual_pieData,
            "allAsset_lineData": allAsset_lineData,
            "discover_lineData": discover_lineData,
            # "cert_listData": cert_listData,
            "sbom_listData": sbom_listData,
            "idle_lineData": idle_lineData,
            "highCpuProc_listData": highCpuProc_listData,
            "highMemProc_listData": highMemProc_listData,
            "highDiskApp_listData": highDiskApp_listData,
            "report_listData_unMgmt_idle": report_listData_unMgmt_idle,
            "report_listData_alarm": report_listData_alarm,
            "report_listData_subnet_isVm": report_listData_subnet_isVm_tf,
            "report_listData_action_tf": report_listData_action_tf,
            "allOnline_donutData": allOnline_donutData,
            "deployToday_barData": deployToday_barData
            }
    else:
        print()
    return RD




