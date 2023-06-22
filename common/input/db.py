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


def plug_in(type):
    try:
        FiveMinuteAgo = (datetime.today() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
        DBSelectTime = (datetime.today() - timedelta(minutes=DBSettingTime)).strftime("%Y-%m-%d %H:%M:%S")
        halfHourAgo = (datetime.today() - timedelta(minutes=35)).strftime("%Y-%m-%d %H:%M:%S")
        yesterday = (datetime.today() - timedelta(1)).strftime("%Y-%m-%d")
        fiveDay = (datetime.today() - timedelta(5)).strftime("%Y-%m-%d")
        weekDay = (datetime.today() - timedelta(7)).strftime("%Y-%m-%d")
        # monthDay = (datetime.today() - timedelta(30)).strftime("%Y-%m-%d")
        monthDay = (datetime.today() - relativedelta(days=31)).strftime("%Y-%m-%d")

        SDL = []
        Conn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHost, DBPort, DBName, DBUser, DBPwd))
        Cur = Conn.cursor()

        # ------------------------------상단 디스크 사용률 도넛 차트------------------------
        if type == 'disk_donutData':
            query = """
                        select 
                            item_count
                        from
                            minutely_statistics
                        where 
                            item = 'Disk Used Percentage#2'
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                    """
        # -----------------------------상단 메모리 사용률 도넛 차트------------------------------
        elif type == 'memory_donutData':
            query = """
                        select 
                            item_count
                        from
                            minutely_statistics
                        where 
                            item = 'Memory Consumption#2'
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                        """
        # -----------------------------상단 씨피유 사용률 도넛 차트------------------------------
        elif type == 'cpu_donutData':
            query = """
                        select 
                            item_count
                        from
                            minutely_statistics
                        where 
                            item = 'CPU Consumption#2'
                            and statistics_collection_date >= '""" + DBSelectTime + """'
            """
        # -----------------------------상단 오에스 파이차트 ------------------------------------
        elif type == 'os_pieData':
            query = """
                        select 
                            item, item_count
                        from
                            minutely_statistics
                        where 
                            classification = 'dashboard_OS Platform'
                            AND item != 'unconfirmed'
                            and NOT item IN ('unconfirmed')
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                        order by item_count desc
                    """
        # -----------------------------상단 유/무선(와이어) 파이차트 ------------------------------------
        elif type == 'wire_pieData':
            query = """
                        select 
                            item, item_count
                        from
                            minutely_statistics
                        where 
                            classification = 'dashboard_wired/wireless 2'
                            AND item != 'unconfirmed'
                            and NOT item IN ('unconfirmed')
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                        order by item_count desc
                    """
        # -----------------------------상단 물리/가상 파이차트 ------------------------------------
        elif type == 'virtual_pieData':
            query = """
                        select 
                            item, item_count
                        from
                            minutely_statistics
                        where 
                            classification = 'dashboard_Is Virtual#3'
                            AND item != 'unconfirmed'
                            and NOT item IN ('unconfirmed')
                            and statistics_collection_date >= '""" + DBSelectTime + """'
                        order by item_count desc
                    """
        # -----------------------------중앙 미관리자산 라인차트 ------------------------------------
        elif type == 'discover_lineData':
            query = """
                        select 
                            TO_CHAR(statistics_collection_date, 'YYYY-MM-DD'), item_count
                        from
                            daily_statistics
                        where 
                            item = 'unmanagement'
                            and statistics_collection_date >= '""" + weekDay + """'
                        order by statistics_collection_date asc
                    """
        #-----------------------------예상 유휴자산 라인차트 ------------------------------------
        elif type == 'idle_lineData':
            query = """
                        select 
                            TO_CHAR(statistics_collection_date, 'YYYY-MM-DD') ,item_count
                        from
                            daily_statistics
                        where 
                            item = 'collection_date'
                            and statistics_collection_date >= '""" + weekDay + """'
                        order by statistics_collection_date asc
                    """
        # -----------------------------인증서리스트 ------------------------------------
        elif type == 'cert_listData':
            query = """
                        select 
                            item, item_count
                        from
                            daily_statistics
                        where
                            classification = 'certificate_list'
                        AND
                            item != 'Root'
                        AND
                            statistics_collection_date >= '""" + yesterday + """'
                        order by 
                            item_count ASC
                        LIMIT 7
                    """
        Cur.execute(query)
        RS = Cur.fetchall()
        for R in RS:
            if type == 'disk_donutData' or type == 'memory_donutData' or type == 'cpu_donutData':
                SDL.append(
                    (
                        ('count', int(R[0]))
                    )
                )
            elif type == 'os_pieData' or type == 'wire_pieData' or type == 'virtual_pieData' or type == 'discover_lineData' or type == 'idle_lineData':
                SDL.append(dict(
                    (
                        ('item', R[0]),
                        ('count', int(R[1]))
                    )
                ))
            elif type == 'cert_listData':
                SDL.append(dict(
                    (
                        ('name', R[0]),
                        ('date', R[1])
                    )
                ))
            else:
                SDL.append(R)
        return SDL
    except Exception as e:
        print(str(type) +'Statistics Table connection(Select) Failure _'+ str(e))
