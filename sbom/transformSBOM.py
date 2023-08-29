import json

with open("setting.json", encoding="UTF-8") as f:
    SETTING = json.loads(f.read())

def sbom_pie_tf(data):
    results = []
    for i in data:
        item_dict = json.loads(i[0])
        comp_name = item_dict['comp_name']
        comp_ver = item_dict['comp_ver']
        if comp_ver is None:
            comp_ver=''
        count = i[1]

        results.append({
            'comp_name': comp_name,
            'comp_ver': comp_ver,
            'count': count
        })
    return results
def sbom_line_tf(data):
    results = []
    for i in data:
        date = i[0]
        count = i[1]

        results.append({
            'date': date,
            'count': count
        })
    return results

def sbom_bar_tf(data):
    results = []
    for i in data:
        ip = i[0]
        count = i[1]

        results.append({
            'ip': ip,
            'count': count
        })
    return results