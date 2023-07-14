def plug_in(data):
    grouped_data = {}
    for d in data:
        key = d['ip']
        if key not in grouped_data:
            grouped_data[key] = {'vm': {'count': 0, 'change': 0},
                                 'pm': {'count': 0, 'change': 0}}

        prefix = d['name'].split('_')[-1]  # vm or pm
        current_count = int(d['count'])

        if grouped_data[key][prefix]['count'] != 0:  # Change is calculated only when previous count exists.
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