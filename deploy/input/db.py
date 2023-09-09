import math

import psycopg2
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import pandas as pd

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
DataLoadingType = SETTING['MODULE']['DataLoadingType']
DBHost = SETTING['DB']['DBHost']
DBPort = SETTING['DB']['DBPort']
DBName = SETTING['DB']['DBName']
DBUser = SETTING['DB']['DBUser']
DBPwd = SETTING['DB']['DBPwd']
AssetTNM = SETTING['DB']['AssetTNM']
StatisticsTNM = SETTING['DB']['StatisticsTNM']
BS = SETTING['FILE']
DBSettingTime = SETTING['DB']['DBSelectTime']
day = datetime.today().strftime("%Y-%m-%d")
RSU = SETTING['FILE']['RunningService_Except']['USE']


def plug_in(table, day, type):
    try:
        FiveMinuteAgo = (datetime.today() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        DBSelectTime = (datetime.today() - timedelta(minutes=DBSettingTime)).strftime("%Y-%m-%d %H:%M:%S")
        halfHourAgo = (datetime.today() - timedelta(minutes=35)).strftime("%Y-%m-%d %H:%M:%S")
        yesterday = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
        fiveDay = (datetime.today() - timedelta(5)).strftime("%Y-%m-%d")
        # monthDay = (datetime.today() - timedelta(30)).strftime("%Y-%m-%d")
        monthDay = (datetime.today() - relativedelta(days=31)).strftime("%Y-%m-%d")
        # ----------------------서버수량그래프 데이터 변경 추가 종윤 ----------------------
        lastYear = (datetime.today() - relativedelta(months=12)).strftime("%Y-%m-%d")
        lastDay = (datetime.today() - relativedelta(months=11)).strftime("%Y-%m-%d")
        lastMonth = pd.date_range(lastDay, periods=12, freq='M').strftime("%Y-%m-%d")
        Reportday2 = (datetime.today() - timedelta(2)).strftime("%Y-%m-%d")
        Reportday = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")

        a = []
        for i in lastMonth:
            a.append(str(i))
        LM = tuple(a)

        # ------------------------------------------------------------------------------
        month_str = (datetime.today() - relativedelta(months=1)).strftime("%Y-%m-%d")
        SDL = []
        Conn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()

        if table == 'action_log':
            query = """
                select
                    package, computer_group, comment, admin, log_collection_date
                from
                    action_log
                order by
                    log_collection_date desc
            """
        elif table == 'action_status':
            query = """
                select deploy_name, action_id, TO_CHAR(action_date, 'YYYY-MM-DD HH24:MI:SS') as action_date, action_result, arcount
                from deploy_status
                order by deploy_collection_date desc
                limit 5
            """
        # if table == 'sbom_paging':
        #     query = """
        #         select
        #             name, version, cpe, type, count
        #         from
        #             sbom_list
        #         where
        #             name != 'Not Scanned'
        #         and
        #             (name Ilike '%""" + type[2] + """%' or
        #             version Ilike '%""" + type[2] + """%' or
        #             cpe Ilike '%""" + type[2] + """%' or
        #             type Ilike '%""" + type[2] + """%' or
        #             count Ilike '%""" + type[2] + """%')
        #         order by
        #             count::INTEGER desc, name asc
        #         LIMIT """ + type[0] + """
        #         OFFSET (""" + type[1] + """ -1) * """ + type[0] + """
        #         """
        # if table == 'sbom_paging_count':
        #     query = """
        #         select
        #             COUNT(*)
        #         from
        #             sbom_list
        #         where
        #             name != 'Not Scanned'
        #         and
        #             (name Ilike '%""" + type[2] + """%' or
        #             version Ilike '%""" + type[2] + """%' or
        #             cpe Ilike '%""" + type[2] + """%' or
        #             type Ilike '%""" + type[2] + """%' or
        #             count Ilike '%""" + type[2] + """%')
        #         """

        Cur.execute(query)
        RS = Cur.fetchall()
        for i, R in enumerate(RS, start=1):
            if day == 'memoryMore' or day == 'diskMore':
                index = (int(type[1]) - 1) * int(type[0]) + i
                SDL.append(dict(
                    (
                        ('index', index),
                        ('ip', R[0]),
                        ('name', R[1]),
                        ('use', R[2]),
                        ('total', R[3]),
                        ('usage', str(R[4]))
                    )
                ))
            elif day == 'sbom':
                index = (int(type[1]) - 1) * int(type[0]) + i
                SDL.append(dict(
                    (
                        ('index', index),
                        ('name', R[0]),
                        ('version', R[1]),
                        ('cpe', R[2]),
                        ('type', R[3]),
                        ('count', R[4])
                    )
                ))
            elif day == 'cpuMore':
                index = (int(type[1]) - 1) * int(type[0]) + i
                SDL.append(dict(
                    (
                        ('index', index),
                        ('ip', R[0]),
                        ('name', R[1]),
                        ('use', R[2]),
                        ('usage', str(R[3]))
                    )
                ))
            elif day == 'osMore' or day == 'serverBandByMore' or day == 'runningServiceMore' or day == 'runningServiceMore2' or day == 'physicalServerMore':
                index = (int(type[1]) - 1) * int(type[0]) + i
                SDL.append(dict(
                    (
                        ('index', index),
                        ('name', R[0]),
                        ('count', R[1]),
                    )
                ))
            elif day == 'gpuServerMore':
                index = (int(type[1]) - 1) * int(type[0]) + i
                SDL.append(dict(
                    (
                        ('index', index),
                        ('ip', R[0]),
                        ('name', R[1]),
                        ('model', R[2]),
                    )
                ))
            elif day == 'alarmCaseMore':
                index = (int(type[1]) - 1) * int(type[0]) + i
                SDL.append(dict(
                    (
                        ('index', index),
                        ('ip', R[0]),
                        ('name', R[1]),
                        ('ramusage', R[2]),
                        ('cpuusage', R[3]),
                        ('driveusage', R[4]),
                        ('date', R[5]),

                    )
                ))

            elif day == 'connectDestinationIpMore':

                index = (int(type[1]) - 1) * int(type[0]) + i

                if R[2] != None:
                    name = R[2]
                else:
                    name = 'undefined'
                SDL.append(dict(
                    (
                        ('index', index),
                        ('ip', R[0]),
                        ('count', R[1]),
                        ('name', name),

                    )
                ))

            elif day == 'connectSourceIpMore':

                index = (int(type[1]) - 1) * int(type[0]) + i
                SDL.append(dict(
                    (
                        ('index', index),
                        ('ip', R[0]),
                        ('name', R[1]),
                        ('count', R[2]),

                    )
                ))
            else:
                SDL.append(R)
        return SDL
    except:
        print(table + str(type) + day + ' Daily Table connection(Select) Failure')
    return