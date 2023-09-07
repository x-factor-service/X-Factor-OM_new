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
        weekDay = (datetime.today() - timedelta(7)).strftime("%Y-%m-%d")
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
                    computer_name, ipv4_address, name, version, type, count
                from
                    sbom_detail
                where
                    cpe = '""" + type + """'
            """
        # --------------------- 전체 sbom 목록 ---------------------------------
        if table == 'sbom_paging':
            column_names = ["name", "version", "path", "type", "count"]
            order_column_name = column_names[int(type[4]) - 1]
            order_direction = type[5]
            query = """
                select
                    name, version, path, type, count
                from
                    sbom_list
                where
                    name != 'Not Scanned' and name != '[too many results]'
                AND
                    (name ILIKE '%""" + type[2] + """%' OR
                    version ILIKE '%""" + type[2] + """%' OR
                    path ILIKE '%""" + type[2] + """%' OR
                    type ILIKE '%""" + type[2] + """%' OR
                    count ILIKE '%""" + type[2] + """%')
                AND
                    (name ILIKE '%""" + type[3] + """%' OR
                    version ILIKE '%""" + type[3] + """%' OR
                    path ILIKE '%""" + type[3] + """%' OR
                    type ILIKE '%""" + type[3] + """%' OR
                    count ILIKE '%""" + type[3] + """%')
                order by
                    CASE 
                        WHEN '""" + order_column_name + """' = 'count' THEN 
                            CAST(count AS INTEGER)
                        ELSE 
                            NULL
                    END """ + order_direction + """,
                    CASE 
                        WHEN '""" + order_column_name + """' = 'name' THEN 
                            name
                        WHEN '""" + order_column_name + """' = 'version' THEN 
                            version
                        WHEN '""" + order_column_name + """' = 'path' THEN 
                            path
                        WHEN '""" + order_column_name + """' = 'type' THEN 
                            type
                        ELSE 
                            NULL
                    END """ + order_direction + """
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
                    path ILIKE '%""" + type[2] + """%' OR
                    type ILIKE '%""" + type[2] + """%' OR
                    count ILIKE '%""" + type[2] + """%')
                AND
                    (name ILIKE '%""" + type[3] + """%' OR
                    version ILIKE '%""" + type[3] + """%' OR
                    path ILIKE '%""" + type[3] + """%' OR
                    type ILIKE '%""" + type[3] + """%' OR
                    count ILIKE '%""" + type[3] + """%')
                """
        # ---------------------------CVE가 탐지된 SBOM 목록 -----------------
        if table == 'cve_in_sbom':
            column_names = ["comp_name", "comp_ver", "cve_id", "score", "detect_time", "detect_count"]
            order_column_index = int(type[3]) - 1
            order_column_name = column_names[order_column_index]
            order_direction = type[4]
            if order_column_name == "score":
                order_by_clause = "CAST(substring(score FROM '\\d+\\.\\d+') AS FLOAT) " + order_direction
            else:
                order_by_clause = order_column_name + " " + order_direction
            query = """
                    SELECT 
                        sbom_cve.comp_name, 
                        sbom_cve.comp_ver, 
                        cve_id, 
                        score,
                        COALESCE(COUNT(sbom_detail.name), 0) AS detect_count,
                        COALESCE(DATE(sbom_detail.sbom_collection_date), (SELECT DATE(MAX(sbom_collection_date)) FROM sbom_detail)) AS detect_time
                    FROM sbom_cve
                    LEFT JOIN sbom_detail
                    ON sbom_cve.comp_name = sbom_detail.name
                    AND sbom_cve.comp_ver = sbom_detail.version
                    WHERE 
                        sbom_cve.comp_name ILIKE '%""" + type[2] + """%' OR
                        sbom_cve.comp_ver ILIKE '%""" + type[2] + """%' OR 
                        cve_id ILIKE '%""" + type[2] + """%' OR 
                        score::text ILIKE '%""" + type[2] + """%'
                    GROUP BY sbom_cve.comp_name, sbom_cve.comp_ver, cve_id, score, sbom_detail.sbom_collection_date
                    ORDER BY """ + order_by_clause + """
                    LIMIT """ + type[0] + """
                    OFFSET (""" + type[1] + """ -1) * """ + type[0] + """
                    """
            # ----------------------- 탐지목록 CVE 개수 -------------------------
        if table == 'cve_in_sbom_count':
            query = """
                    SELECT 
                        count(*)
                    FROM (
                        SELECT sbom_cve.comp_name, sbom_cve.comp_ver, cve_id, score
                        FROM sbom_cve
                        LEFT JOIN sbom_detail
                        ON sbom_cve.comp_name = sbom_detail.name
                        AND sbom_cve.comp_ver = sbom_detail.version
                        WHERE 
                            sbom_cve.comp_name ILIKE '%""" + type[2] + """%' OR
                            sbom_cve.comp_ver ILIKE '%""" + type[2] + """%' OR 
                            cve_id ILIKE '%""" + type[2] + """%' OR 
                            score::text ILIKE '%""" + type[2] + """%'
                        GROUP BY sbom_cve.comp_name, sbom_cve.comp_ver, cve_id, score
                        ) 
                    AS derived_table;
                    """
        # ------ SBOM 더보기
        if table == 'cve_detail':
            query = """
                WITH DetailCount AS (
                    SELECT 
                        sd.name,
                        sd.version,
                        COUNT(*) AS detect_count,
                        MAX(DATE(sd.sbom_collection_date)) AS latest_collection_date
                    FROM sbom_detail sd
                    JOIN sbom_cve sc ON sd.name = sc.comp_name AND sd.version = sc.comp_ver
                    WHERE sc.cve_id = '""" + type[0] + """' AND sc.comp_name = '""" + type[1] + """' AND sc.comp_ver = '""" + type[2] + """'
                    GROUP BY sd.name, sd.version
                )                
                SELECT
                    sc.comp_name,
                    sc.comp_ver,
                    sc.cve_id,
                    sc.score,
                    sc.note,
                    sc.solution,
                    COALESCE(dc.latest_collection_date, (SELECT DATE(MAX(sbom_collection_date)) FROM sbom_detail)) AS detect_time,
                    COALESCE(dc.detect_count, 0) AS detect_count
                FROM sbom_cve sc
                LEFT JOIN DetailCount dc ON sc.comp_name = dc.name AND sc.comp_ver = dc.version
                WHERE sc.cve_id = '""" + type[0] + """' AND sc.comp_name = '""" + type[1] + """' AND sc.comp_ver = '""" + type[2] + """';
            """
        if table == 'asset_detail':
            column_names = ["computer_name", "ipv4_address", "name", "version", "path", "type"]
            order_column_name = column_names[int(type[6]) - 1]
            order_direction = type[7]
            query = """
                SELECT
                    sd.computer_name,
                    sd.ipv4_address,
                    sd.name,
                    sd.version,
                    sd.path,
                    sd.type
                FROM sbom_detail sd
                JOIN sbom_cve sc ON sd.name = sc.comp_name AND sd.version = sc.comp_ver
                WHERE sc.cve_id = '""" + type[0] + """' AND sc.comp_name = '""" + type[1] + """' AND sc.comp_ver = '""" + type[2] + """'
                AND
                    (sd.computer_name ILIKE '%""" + type[5] + """%' OR
                    sd.ipv4_address ILIKE '%""" + type[5] + """%' OR
                    sd.name ILIKE '%""" + type[5] + """%' OR
                    sd.version ILIKE '%""" + type[5] + """%' OR
                    sd.path ILIKE '%""" + type[5] + """%' OR
                    sd.type ILIKE '%""" + type[5] + """%')
                order by
                    """ + order_column_name + """ """ + order_direction + """
                LIMIT """ + type[3] + """
                OFFSET (""" + type[4] + """ -1) * """ + type[3] + """         
            """
        if table == 'asset_detail_count':
            query = """
                SELECT COUNT(*)
                FROM sbom_detail sd
                JOIN sbom_cve sc ON sd.name = sc.comp_name AND sd.version = sc.comp_ver
                WHERE sc.cve_id = '""" + type[0] + """' AND sc.comp_name = '""" + type[1] + """' AND sc.comp_ver = '""" + type[2] + """'
                AND
                    (sd.computer_name ILIKE '%""" + type[5] + """%' OR
                    sd.ipv4_address ILIKE '%""" + type[5] + """%' OR
                    sd.name ILIKE '%""" + type[5] + """%' OR
                    sd.version ILIKE '%""" + type[5] + """%' OR
                    sd.path ILIKE '%""" + type[5] + """%' OR
                    sd.type ILIKE '%""" + type[5] + """%')           
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
                                LOWER(sbom_list.name) = LOWER(sbom_cve.comp_name)
                                AND
                                LOWER(sbom_list.version) = LOWER(sbom_cve.comp_ver)
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
                                LOWER(sbom_list.name) = LOWER(sbom_cve.comp_name)
                                AND
                                LOWER(sbom_list.version) = LOWER(sbom_cve.comp_ver)
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
                    where classification = 'sbom_pie_data'
                    ORDER BY CAST(item_count AS INTEGER) DESC
            """
        # ---------------------Sbom line 차트------------------------
        if table == 'sbom_lineData':
            query = """
                select TO_CHAR(statistics_collection_date, 'YYYY-MM-DD') AS statistics_collection_date,item_count
                from """ + StatisticsSBOM + """
                where classification = 'sbom_line_data'
                and statistics_collection_date >= '""" + weekDay + """'
                order by statistics_collection_date asc
                limit 7
            """

        # ---------------------sbom bar 차트 ----------------------------
        if table == 'sbom_barData':
            query = """
                    SELECT item, item_count 
                    from """ + StatisticsSBOM + """
                    where classification = 'sbom_bar_data'
                    ORDER BY CAST(item_count AS INTEGER) DESC
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
                        ('path', R[2]),
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
                        ('detect_count', R[4]),
                        ('detect_time', R[5])
                    )
                ))
            elif day == 'cve_detail':
                SDL.append(dict(
                    (
                        ('comp_name', R[0]),
                        ('comp_ver', R[1]),
                        ('cve_id', R[2]),
                        ('score', R[3]),
                        ('note', R[4]),
                        ('solution', R[5]),
                        ('detect_time', R[6]),
                        ('detect_count', R[7])
                    )
                ))
            elif day == 'asset_detail':
                index = (int(type[4]) - 1) * int(type[3]) + i
                SDL.append(dict(
                    (
                        ('index', index),
                        ('computer_name', R[0]),
                        ('ipv4_address', R[1]),
                        ('name', R[2]),
                        ('version', R[3]),
                        ('path', R[4]),
                        ('type', R[5])
                    )
                ))
            else:
                SDL.append(R)
        return SDL
    except:
        print(table + str(type) + day + ' Daily Table connection(Select) Failure')
    return