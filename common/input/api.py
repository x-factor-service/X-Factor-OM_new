import requests
import json
import logging
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from pprint import pprint

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
APIURL = SETTING['API']['apiUrl']
SKP = SETTING['API']['PATH']['SessionKey']
APIUNM = SETTING['API']['username']
APIPWD = SETTING['API']['password']

def session() :
    logger = logging.getLogger(__name__)
    try:
        SKH = '{"username": "'+APIUNM+'", "domain": "", "password": "'+APIPWD+'"}'
        SKURL = APIURL + SKP
        SKR = requests.post(SKURL, data=SKH, verify=False)
        SKRC = SKR.status_code
        SKRT = SKR.content.decode('utf-8')
        SKRJ = json.loads(SKRT)
        SK = SKRJ['data']['session']
        logger.info('Tanium API Session Key 호출 성공')
        logger.info('Session Key : '+str(SK))
        return SK
    except :
        logger.warning('Tanium API Session Key 호출 Error 발생')

# 대시보드, 상단, 원형 차트 다섯개
# endpoints의 first 값이 최대 1000개로 1000개 까지의 값만 불러올 수 있음.
def top_donut() :
    SK=session()
    url = "https://192.168.5.100/plugin/products/gateway/graphql"  # API 엔드포인트 URL
    query = """
    query getTDSEndpoint {
      endpoints (after: null, first: 1000) {
        edges {
          node {
            id
            computerID
            sensorReadings(
              sensors: [{name: "Computer Name"},{name: "Computer ID"},{name:"Disk Used Percentage#2"},{name:"Memory Consumption#2"},{name:"CPU Consumption#2"},{name:"OS Platform"},{name:"Is Virtual#3"},{name:"wired/wireless 2"}]
            ) {
              columns {
                name
                values
                sensor {
                  name
                }
              }
            }
          }
        }
      }
    }
        """
    response = requests.post(url,headers={"session":SK}, json={"query": query}, verify=False)
    if response.status_code == 200:
        data = response.json()['data']['endpoints']['edges']
        return data
    else:
        print("API 요청 실패:", response.text)


