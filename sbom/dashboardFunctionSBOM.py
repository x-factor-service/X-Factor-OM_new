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

#####################################  OM페이지  ################################################
def DashboardData():
    logger = logging.getLogger(__name__)
    if Customer == 'NC' or Customer == 'Xfactor':
        if ProjectType == 'System':
            if core == 'Tanium':
                sbom_package_list = []
                # try:
                #     sbom_package = SDPI('sbom', '', '')
                #     for i in range(len(sbom_package)):
                #         sbom_package_list.append({'name': sbom_package[i][0], 'version': sbom_package[i][1], 'cpe': sbom_package[i][2],
                #                                 'type': sbom_package[i][3], 'count': sbom_package[i][4]})
                # except:
                #     print("No")
                # NC 대역벌 서버수량 chart
                try:
                    SBCQ = PDPI('statistics', 'today', 'group_server_count')
                    server_BChartDataList = CTDF(SBCQ, 'bar')
                    if not SBCQ:
                        server_BChartDataList = [{"name": "-", "value": 0}]
                    logger.info('dashboard_function.py - server_BChartDataList - Success')
                except:
                    logger.warning('dashboard_function.py - Error Occurred')
                    logger.warning('Error - server_BChartDataList')



                SBDL = sbom_package_list

            elif core == 'Zabbix':
                print()
        elif ProjectType == 'Service':
            print()

        RD = {
            "sbom_package_list": SBDL

        }

    else:
        if ProjectType == 'System':
            if core == 'Tanium':

                BCQ = PDPI('statistics', 'today', 'bar')
                BChartDataList = CTDF(BCQ, 'bar')

                PCQ = PDPI('statistics', 'today', 'pie')
                PChartDataList = CTDF(PCQ, 'pie')

                LG = PDPI('statistics', "assetItem", "Group")
                # print(LG)
                LINEGROUP = CTDF(LG, 'group')

                LCQ = PDPI('statistics', 'fiveDay', 'asset')
                LNFD = [LCQ, LINEGROUP]
                # print(LCQ)

                ESAIDL = TDLC(LNFD)
                # print(ESAIDL)
                LChartDataList = TDCD(ESAIDL, "Line")
                # print(LChartDataList)

                DCQ = PDPI('statistics', 'today', 'donut')
                DChartDataList = CTDF(DCQ, 'donut')
                # EAYL = IDPI('asset', 'yesterday', '')
                # print(EAML)

                # banner chart
                BNY = PDPI('statistics', 'yesterday', '')
                # print(BNY)
                TSDLY = TDBA(BNY, 'yetoday')
                # print(TSDLY)
                BNT = PDPI('statistics', 'today', '')
                # print(BNT)
                TSDLT = TDBA(BNT, 'yetoday')
                # print(TSDLT)
                SBNDL = ASDC(TSDLY, TSDLT)
                # print(SBNDL)
                BNChartDataList = TDCD(SBNDL, 'Banner')
                # print(BNChartDataList)

                ACDT = PDPI('statistics_list', 'today', 'statistics')
                # print(ACDT)

                # alarmcase chart
                RD = ACDF(ACDT, 'alarmTotal')
                RDCase = {'nodeDataList': RD}

                RDL = ACDF(ACDT, 'alarmTop')
                # print(RDL)
                RDLCase = {'nodeDataList': RDL}
                # print(RDLCase)
                # TATA = nodeDataListx + nodeDataList
                # print(RDCase)

                # ram, cpu 사용량 초과 mini donut
                MDRC = PDPI('statistics', '', 'ram')
                MDCC = PDPI('statistics', '', 'cpu')

                Ramdonut = USDF(MDRC, 'ram')
                Cpudonut = USDF(MDCC, 'cpu')

                MDRCC = Ramdonut + Cpudonut

                # worldMap alarmCase
                WMQ = PDPI('statistics', '', 'world')
                WMAC = WDDF(WMQ)

                # radar chart
                RCList = RDDF(ACDT)
                RACA = {'nodeDataList': RDL + RCList}

                BDL = BChartDataList
                LDL = LChartDataList
                PDL = PChartDataList
                BNDL = BNChartDataList
                ALDL = [[]]
                NCDL = RACA
                TACC = RDCase
                TACT = RDLCase
                WMCDL = [WMAC]
                MDRU = []
                DDLC = DChartDataList

            elif core == 'Zabbix':
                print()
        elif ProjectType == 'Service':
            print()
        RD = {
            "barChartData": BDL,
            "lineChartData": LDL,
            "pieChartData": PDL,
            "bannerData": BNDL,
            "alarmListData": ALDL[0],
            "AssociationDataList": NCDL,
            "TotalDataList": TACC,
            "TotalTopDataList": TACT,
            "WorldMapDataList": WMCDL,
            "MiniDonutChart": MDRCC,
            "donutChartDataList": DDLC
        }
    return RD




