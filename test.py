import requests
import json
import logging
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())
APIURL = SETTING['API']['apiUrl']
SKP = SETTING['API']['PATH']['SessionKey']
APIUNM = SETTING['API']['username']
APIPWD = SETTING['API']['password']

def test():
    SKH = '{"username": "' + APIUNM + '", "domain": "", "password": "' + APIPWD + '"}'
    SKURL = APIURL + SKP
    SKR = requests.post(SKURL, data=SKH, verify=False)
    SKRC = SKR.status_code
    SKRT = SKR.content.decode('utf-8', errors='ignore')
    SKRJ = json.loads(SKRT)
    SK = SKRJ['data']['session']

    url = "https://192.168.5.100/plugin/products/gateway/graphql"  # API 엔드포인트 URL
    query = """
    query getTDSEndpoint {
      endpoints {
        edges {
          node {
            id
            computerID
            sensorReadings(
              sensors: [{name: "Computer Name"},{name: "Computer ID"},{name:"Disk Used Percentage#2"},{name:"Memory Consumption#2"},{name:"CPU Consumption#2"},{name:"OS Platform"},{name:"Is Virtual"},{name:"wired/wireless 2"}]
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
        """  # 실행할 쿼리

    response = requests.post(url,headers={"session":SK}, json={"query": query}, verify=False)

    if response.status_code == 200:
        data = response.json()
        print(data)
        # 데이터 처리
        # 예: data['data']['yourQueryName']['field1']
    else:
        print("API 요청 실패:", response.text)

test()