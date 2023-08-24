from datetime import datetime, timedelta
import json

#----------------------------------OM 일일 리포트 vm/pm--------------------------------------------------------
def plug_in(data):
    grouped_data = {}
    for d in data:
        key = d['ip']
        if key not in grouped_data:
            grouped_data[key] = {'vm': {'count': 0, 'change': 0},
                                 'pm': {'count': 0, 'change': 0}}

        prefix = d['name'].split('_')[-1]
        current_count = int(d['count'])

        if grouped_data[key][prefix]['count'] != 0:
            grouped_data[key][prefix]['change'] = current_count - grouped_data[key][prefix]['count']
        grouped_data[key][prefix]['count'] = current_count

    result = []
    for ip, info in grouped_data.items():
        result.append({
            'ip': ip,
            'daily_om_vm': info['vm']['count'],
            'vm_change': info['vm']['change'],
            'daily_om_pm': info['pm']['count'],
            'pm_change': info['pm']['change']
        })
    return result

#----------------------------------일일 리포트 배포 성공 패키지 -----------------------------------
def plug_in_action(data):
    result = {}
    for item in data:
        key = (item['user'], item['package'], item['group'])
        if key not in result:
            result[key] = {'user': item['user'], 'package': item['package'], 'group': item['group'], 'count': 0}
        result[key]['count'] += 1
    result = list(result.values())
    return result

def plug_in_number(data):
    result = data[0][0]
    return result
