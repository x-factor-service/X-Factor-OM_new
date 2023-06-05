import logging

from common.transform import transform_donutData, transform_pieData
import urllib3
import json
import math

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
core = SETTING['PROJECT']['CORE']
ProjectType = SETTING['PROJECT']['TYPE']
Customer = SETTING['PROJECT']['CUSTOMER']

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#####################################  메인 대시보드 페이지  ################################################
def Dashboard():
    logger = logging.getLogger(__name__)
    if Customer == 'NC' or Customer == 'Xfactor':
        disk_donutData = []
        memory_donutData = []
        cpu_donutData = []
        wire_pieData = []
        os_pieData = []
        virtual_pieData = []
        discover_lineData = []
        cert_listData = []
        sbom_listData = []
        report_listData = []
        idle_lineData = []


            #------------------------------상단 디스크 사용률 도넛 차트------------------------
        try:
            disk_donutData = transform_donutData('Disk Used Percentage#2')
            logger.info('dashboardFunction.py - disk_donutData - Success')
        except:
            logger.warning('dashboardFunction.py - Error Occurred')
            logger.warning('Error - disk_donutData')

            # -----------------------------상단 메모리 사용률 도넛 차트------------------------------
        try:
            memory_donutData = transform_donutData('Memory Consumption#2')
            logger.info('dashboardFunction.py - memory_donutData - Success')
        except:
            logger.warning('dashboardFunction.py - Error Occurred')
            logger.warning('Error - memory_donutData')
            # -----------------------------상단 씨피유 사용률 도넛 차트------------------------------
        try:
            cpu_donutData = transform_donutData('CPU Consumption#2')
            logger.info('dashboardFunction.py - cpu_donutData - Success')
        except:
            logger.warning('dashboardFunction.py - Error Occurred')
            logger.warning('Error - cpu_donutData')
            # -----------------------------상단 오에스 파이차트 ------------------------------------
        try:
            os_pieData = transform_pieData('OS Platform')
            logger.info('dashboardFunction.py - os_pieData - Success')
        except:
            logger.warning('dashboardFunction.py - Error Occurred')
            logger.warning('Error - os_pieData')
            # -----------------------------상단 유/무선(와이어) 파이차트 ------------------------------------
        try:
            wire_pieData = transform_pieData('wired/wireless 2')
            logger.info('dashboardFunction.py - wire_pieData - Success')
        except:
            logger.warning('dashboardFunction.py - Error Occurred')
            logger.warning('Error - wire_pieData')
            # -----------------------------상단 물리/가상 파이차트 ------------------------------------
        try:
            virtual_pieData = transform_pieData('Is Virtual#3')
            logger.info('dashboardFunction.py - virtual_pieData - Success')
        except:
            logger.warning('dashboardFunction.py - Error Occurred')
            logger.warning('Error - virtual_pieData')

        RD = {
            'disk_donutData': disk_donutData,
            'memory_donutData': memory_donutData,
            'cpu_donutData': cpu_donutData,
            'wire_pieData': wire_pieData,
            "os_pieData": os_pieData,
            "virtual_pieData": virtual_pieData,
            "discover_lineData": discover_lineData,
            "cert_listData": cert_listData,
            "sbom_listData": sbom_listData,
            "report_listData": report_listData,
            "idle_lineData": idle_lineData
            }
    else:
        print()
    return RD




