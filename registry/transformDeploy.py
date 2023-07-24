import pandas as pd
import json
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
AlarmRamUsage = SETTING['PROJECT']['Alarm']['RamUsage']
alarmCaseFirst = SETTING['PROJECT']['Alarm']['Case']['First']
alarmCaseSecond = SETTING['PROJECT']['Alarm']['Case']['Second']
alarmCaseThird = SETTING['PROJECT']['Alarm']['Case']['Third']
alarmCaseFourth = SETTING['PROJECT']['Alarm']['Case']['Fourth']
alarmCaseFifth = SETTING['PROJECT']['Alarm']['Case']['Fifth']
alarmCaseSix = SETTING['PROJECT']['Alarm']['Case']['Six']
alarmCaseSeven = SETTING['PROJECT']['Alarm']['Case']['Seven']


def transform(data, user):
    DFL = []
    columns = ['package', 'computer_group', 'comment', 'admin', 'creation_date']
    PCK = data['data']['package_spec']['name']
    CG = data['data']['target_group']['name']
    CMM = 'success!'
    AD = user
    CD = datetime.strptime(data['data']['creation_time'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
    # CD = datetime.strptime(data['data']['creation_time'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")
    DFL.append([PCK, CG, CMM, AD, CD])
    df = pd.DataFrame(DFL, columns=columns)
    pd.set_option('display.expand_frame_repr', False)
    return df



