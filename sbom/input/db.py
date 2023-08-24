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
StatisticsSBOM = SETTING['DB']['StatisticsSBOM']

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

        if table == 'sbom_detail':
            query = """
                select
                    computer_name, ipv4_address, name, version, type, path, count
                from
                    sbom_detail
                where
                    cpe = '""" + type + """'
            """
        # --------------------- 전체 sbom 목록 ---------------------------------
        if table == 'sbom_paging':
            column_names = ["name", "version", "cpe", "type", "count"]
            order_column_name = column_names[int(type[4]) - 1]
            order_direction = type[5]

            query = """
                select
                    name, version, cpe, type, count
                from
                    sbom_list
                where
                    name != 'Not Scanned' and name != '[too many results]'
                AND
                    (name ILIKE '%""" + type[2] + """%' OR
                    version ILIKE '%""" + type[2] + """%' OR
                    cpe ILIKE '%""" + type[2] + """%' OR
                    type ILIKE '%""" + type[2] + """%' OR
                    count ILIKE '%""" + type[2] + """%')
                AND
                    (name ILIKE '%""" + type[3] + """%' OR
                    version ILIKE '%""" + type[3] + """%' OR
                    cpe ILIKE '%""" + type[3] + """%' OR
                    type ILIKE '%""" + type[3] + """%' OR
                    count ILIKE '%""" + type[3] + """%')
                order by
                    """ + order_column_name + """ """ + order_direction + """
                LIMIT """ + type[0] + """
                OFFSET (""" + type[1] + """ -1) * """ + type[0] + """
                """
        # ------------------------------ 전체 sbom 목록 개수 -------------------------
        if table == 'sbom_paging_count':
            query = """
                select
                    COUNT(*)
                from
                    sbom_list
                where
                    name != 'Not Scanned'
                                AND
                    (name ILIKE '%""" + type[2] + """%' OR
                    version ILIKE '%""" + type[2] + """%' OR
                    cpe ILIKE '%""" + type[2] + """%' OR
                    type ILIKE '%""" + type[2] + """%' OR
                    count ILIKE '%""" + type[2] + """%')
                AND
                    (name ILIKE '%""" + type[3] + """%' OR
                    version ILIKE '%""" + type[3] + """%' OR
                    cpe ILIKE '%""" + type[3] + """%' OR
                    type ILIKE '%""" + type[3] + """%' OR
                    count ILIKE '%""" + type[3] + """%')
                """
        #----------------------- 전체 CVE 목록 --------------------------------
        if table == 'sbom_cve':
            column_names = ["comp_name", "comp_ver", "cve_id", "score", "vuln_last_reported", "number"]
            order_column_index = int(type[3]) - 1
            order_column_name = column_names[order_column_index]
            order_direction = type[4]

            if order_column_name == "score":
                order_by_clause = "CAST(substring(score FROM '\\d+\\.\\d+') AS FLOAT) " + order_direction
            else:
                order_by_clause = order_column_name + " " + order_direction
            query = """
                select
                    comp_name, comp_ver, cve_id, score, vuln_last_reported, number, note, solution
                from
                    sbom_cve
                where
                    comp_name Ilike '%""" + type[2] + """%' or
                    comp_ver Ilike '%""" + type[2] + """%' or
                    cve_id Ilike '%""" + type[2] + """%' or
                    score Ilike '%""" + type[2] + """%' or
                    vuln_last_reported Ilike '%""" + type[2] + """%'
                order by """ + order_by_clause + """
                LIMIT """ + type[0] + """
                OFFSET (""" + type[1] + """ -1) * """ + type[0] + """           
            """

        # --------------------------------- 전체 CVE 목록 개수 --------------------------------
        if table == 'sbom_cve_count':
            query = """
                select
                    count(*)
                from
                    sbom_cve
                where
                    comp_name Ilike '%""" + type[2] + """%' or
                    comp_ver Ilike '%""" + type[2] + """%' or
                    cve_id Ilike '%""" + type[2] + """%' or
                    score Ilike '%""" + type[2] + """%' or
                    vuln_last_reported Ilike '%""" + type[2] + """%'         
            """
        # ---------------------------탐지목록 CVE 데이터 -----------------
        if table == 'cve_in_sbom':
            column_names = ["comp_name", "comp_ver", "cve_id", "score", "vuln_last_reported", "number"]
            order_column_index = int(type[3]) - 1
            order_column_name = column_names[order_column_index]
            order_direction = type[4]
            if order_column_name == "score":
                order_by_clause = "CAST(substring(score FROM '\\d+\\.\\d+') AS FLOAT) " + order_direction
            else:
                order_by_clause = order_column_name + " " + order_direction
            query = """
                SELECT 
                    comp_name, comp_ver, cve_id, score, vuln_last_reported, number, note, solution
                FROM sbom_cve
                WHERE EXISTS (
                    SELECT 1
                    FROM sbom_list
                    WHERE
                    (
                        (sbom_list.name ILIKE CONCAT('%', sbom_cve.comp_name, '%') OR sbom_list.version ILIKE CONCAT('%', sbom_cve.comp_name, '%'))
                        AND
                        (sbom_list.name ILIKE CONCAT('%', sbom_cve.comp_ver, '%') OR sbom_list.version ILIKE CONCAT('%', sbom_cve.comp_ver, '%'))
                    )
                )
                AND
                    (
                    comp_name Ilike '%""" + type[2] + """%' or
                    comp_ver Ilike '%""" + type[2] + """%' or
                    cve_id Ilike '%""" + type[2] + """%' or
                    score Ilike '%""" + type[2] + """%' or
                    vuln_last_reported Ilike '%""" + type[2] + """%'
                    )
                order by """ + order_by_clause + """
                LIMIT """ + type[0] + """
                OFFSET (""" + type[1] + """ -1) * """ + type[0] + """
            """
            # ----------------------- 탐지목록 CVE 개수 -------------------------
        if table == 'cve_in_sbom_count':
            query="""
                SELECT 
                    COUNT(*)
                FROM sbom_cve
                                WHERE EXISTS (
                    SELECT 1
                    FROM sbom_list
                    WHERE
                    (
                        (sbom_list.name ILIKE CONCAT('%', sbom_cve.comp_name, '%') OR sbom_list.version ILIKE CONCAT('%', sbom_cve.comp_name, '%'))
                        AND
                        (sbom_list.name ILIKE CONCAT('%', sbom_cve.comp_ver, '%') OR sbom_list.version ILIKE CONCAT('%', sbom_cve.comp_ver, '%'))
                    )
                )
                AND
                (
                    comp_name Ilike '%""" + type[2] + """%' or
                    comp_ver Ilike '%""" + type[2] + """%' or
                    cve_id Ilike '%""" + type[2] + """%' or
                    score Ilike '%""" + type[2] + """%' or
                    vuln_last_reported Ilike '%""" + type[2] + """%'
                )
            """

        # ----------------------------- 탐지 목록 sbom 데이터 -------------------------------
        if table == 'sbom_in_cve':
            column_names = ["name", "version", "cpe", "type", "count"]
            order_column_name = column_names[int(type[3]) - 1]
            order_direction = type[4]
            query = """
                        SELECT name, version, cpe, type, count
                        FROM sbom_list
                        WHERE EXISTS (
                            SELECT 1
                            FROM sbom_cve
                            WHERE
                            (
                                (sbom_list.name ILIKE CONCAT('%', sbom_cve.comp_name, '%') OR sbom_list.version ILIKE CONCAT('%', sbom_cve.comp_name, '%'))
                                AND
                                (sbom_list.name ILIKE CONCAT('%', sbom_cve.comp_ver, '%') OR sbom_list.version ILIKE CONCAT('%', sbom_cve.comp_ver, '%'))
                            )
                        )
                        AND
                            (
                            name Ilike '%""" + type[2] + """%' or
                            version Ilike '%""" + type[2] + """%' or
                            cpe Ilike '%""" + type[2] + """%' or
                            type Ilike '%""" + type[2] + """%' or
                            count Ilike '%""" + type[2] + """%'
                            )
                        order by 
                            """ + order_column_name + """ """ + order_direction + """
                        LIMIT """ + type[0] + """
                        OFFSET (""" + type[1] + """ -1) * """ + type[0] + """
                    """
        # --------------------- 탐지 목록 Sbom 개수 ------------------------------
        if table == 'sbom_in_cve_count':
            query = """
                        SELECT 
                            COUNT(*)
                        FROM sbom_list
                        WHERE EXISTS (
                            SELECT 1
                            FROM sbom_cve
                            WHERE
                            (
                                (sbom_list.name ILIKE CONCAT('%', sbom_cve.comp_name, '%') OR sbom_list.version ILIKE CONCAT('%', sbom_cve.comp_name, '%'))
                                AND
                                (sbom_list.name ILIKE CONCAT('%', sbom_cve.comp_ver, '%') OR sbom_list.version ILIKE CONCAT('%', sbom_cve.comp_ver, '%'))
                            )
                        )
                        AND
                        (
                            name Ilike '%""" + type[2] + """%' or
                            version Ilike '%""" + type[2] + """%' or
                            cpe Ilike '%""" + type[2] + """%' or
                            type Ilike '%""" + type[2] + """%' or
                            count Ilike '%""" + type[2] + """%'
                        )
                    """
        # -----------------SBOM 탐지 파이 차트--------------------
        if table == 'sbom_pieData':
            query = """
                    SELECT item, item_count 
                    from """ + StatisticsSBOM + """
                    where classification = 'sbom_cve'
                    ORDER BY item_count DESC
            """
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
            elif day == 'sbom' or day == 'sbom_in_cve':
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
            elif day == 'cve_in_sbom' or day == 'sbom_cve':
                index = (int(type[1]) - 1) * int(type[0]) + i
                SDL.append(dict(
                    (
                        ('index', index),
                        ('comp_name', R[0]),
                        ('comp_ver', R[1]),
                        ('cve_id', R[2]),
                        ('score', R[3]),
                        ('vuln_last_reported', R[4]),
                        ('number', R[5]),
                        ('note', R[6]),
                        ('solution', R[7])
                    )
                ))
            else:
                SDL.append(R)
        return SDL
    except:
        print(table + str(type) + day + ' Daily Table connection(Select) Failure')
    return