from datetime import datetime, timedelta
import psycopg2
import json
import logging
from tqdm import tqdm

def plug_in(data, cycle):
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        DBHOST = SETTING['DB']['DBHost']
        DBPORT = SETTING['DB']['DBPort']
        DBNM = SETTING['DB']['DBName']
        DBUNM = SETTING['DB']['DBUser']
        DBPWD = SETTING['DB']['DBPwd']
        TNM = SETTING['DB']['LOG']

        today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        insertConn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
        insertCur = insertConn.cursor()

        if cycle == 'action_log':
            IQ = """
                INSERT INTO """ + TNM + """ (
                    package, computer_group, comment, admin, creation_date, log_collection_date
                ) VALUES (
                    %s, %s, %s, %s, %s, '""" + today + """'
                )
            """


        for i in range(len(data.package)):
            PA = data.package[i]
            CG = data.computer_group[i]
            CM = data.comment[i]
            AD = data.admin[i]
            CD = data.creation_date[i]

            dataList = PA, CG, CM, str(AD), CD
            #print(dataList)
            insertCur.execute(IQ, (dataList))
        insertConn.commit()
        insertConn.close()
        logger.info('action_log Table INSERT connection - 성공')
    except ConnectionError as e:
        logger.warning('action_log Table INSERT connection 실패')
        logger.warning('Error : ' + str(e))

def deploy_status(data):
    logger = logging.getLogger(__name__)
    try:
        with open("setting.json", encoding="UTF-8") as f:
            SETTING = json.loads(f.read())
        DBHOST = SETTING['DB']['DBHost']
        DBPORT = SETTING['DB']['DBPort']
        DBNM = SETTING['DB']['DBName']
        DBUNM = SETTING['DB']['DBUser']
        DBPWD = SETTING['DB']['DBPwd']
        AR = SETTING['DB']['DS']

        today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

        insertConn = psycopg2.connect(
            'host={0} port={1} dbname={2} user={3} password={4}'.format(DBHOST, DBPORT, DBNM, DBUNM, DBPWD))
        insertCur = insertConn.cursor()


        IQ = """
            insert into """ + AR + """ (
                deploy_name, action_id, action_date, action_result, arcount, deploy_collection_date
                ) values (
                    %s, %s, %s, %s, %s,'""" + today + """'
                )
        """

        PA = data[0]
        CG = data[1]
        CM = data[2]
        AD = data[3]
        AC = data[4]

        dataList = PA, CG, CM, str(AD), str(AC)
            # print(dataList)
        insertCur.execute(IQ, (dataList))
        insertConn.commit()
        insertConn.close()
        logger.info('action_log Table INSERT connection - 성공')
    except ConnectionError as e:
        logger.warning('action_log Table INSERT connection 실패')
        logger.warning('Error : ' + str(e))
