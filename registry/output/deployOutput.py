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

        today = datetime.today().strftime("%Y-%m-%d")

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
        print(data.package)
        print(data.package[0])
        for i in range(len(data.package)):
            PA = data.package[i]
            CG = data.computer_group[i]
            CM = data.comment[i]
            AD = data.admin[i]
            CD = data.creation_date[i]

            dataList = PA, CG, CM, str(AD), CD
            print(dataList)
            insertCur.execute(IQ, (dataList))
        insertConn.commit()
        insertConn.close()
        logger.info('action_log Table INSERT connection - 성공')
    except ConnectionError as e:
        logger.warning('action_log Table INSERT connection 실패')
        logger.warning('Error : ' + str(e))
