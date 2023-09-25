import logging
from om.transformOM import banner as TDBA, line_chart as TDLC, chart_data as TDCD
from om.transformOM import calculation as ASDC
from om.dataFrameOM import alarmCase as ACDF
from om.dataFrameOM import usage as USDF
from om.dataFrameOM import worldMap as WDDF
from om.dataFrameOM import worldMapNC as WDDFNC
from om.dataFrameOM import radar as RDDF
from om.dataFrameOM import chart as CTDF
from om.input.db import plug_in as PDPI
from sbom.transformSBOM import sbom_pie_tf
from sbom.transformSBOM import sbom_bar_tf
from sbom.transformSBOM import sbom_line_tf
from sbom.input.db import plug_in as SDPI
from collections import Counter
import urllib3
import json
import math

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
core = SETTING['PROJECT']['CORE']
ProjectType = SETTING['PROJECT']['TYPE']
Customer = SETTING['PROJECT']['CUSTOMER']

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def DashboardData():
    logger = logging.getLogger(__name__)
    if Customer == 'NC' or Customer == 'Xfactor':
        sbom_package_list = []
        sbom_pieData = []
        sbom_barData = []
        try:
            SBDL = sbom_package_list
            logger.info('dashboardFunctionSBOM.py - sbom_package_list - Success')
        except:
            logger.warning('dashboardFunctionSBOM.py - Error Occurred')
            logger.warning('Error - sbom_package_list')

        #--------------SBOM에서 탐지된 취약 패키지----------------
        try:
            sbom_pieData_input = SDPI('sbom_pieData', '', '')
            sbom_pieData = sbom_pie_tf(sbom_pieData_input)
            logger.info('dashboardFunctionSBOM.py - sbom_pieData - Success')
        except:
            logger.warning('dashboardFunctionSBOM.py - Error Occurred')
            logger.warning('Error - sbom_pieData')
        # -------------- SBOM line chart ------------------------
        try:
            sbom_lineData_input = SDPI('sbom_lineData', '', '')
            sbom_lineData = sbom_line_tf(sbom_lineData_input)
        except:
            logger.warning('dashboardFunctionSBOM.py - Error Occurred')
            logger.warning('Error - sbom_lineData')
        #-------------- SBOM bar chart ------------------------
        try:
            sbom_barData_input = SDPI('sbom_barData', '', '')
            sbom_barData = sbom_bar_tf(sbom_barData_input)
        except:
            logger.warning('dashboardFunctionSBOM.py - Error Occurred')
            logger.warning('Error - sbom_barData')

        RD = {
            "sbom_package_list": SBDL,
            "sbom_pieData": sbom_pieData,
            "sbom_lineData": sbom_lineData,
            "sbom_barData": sbom_barData
        }
    return RD




