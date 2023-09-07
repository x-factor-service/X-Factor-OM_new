def sbom_pie_tf(data):
    results = []
    for item in data:

        parts = item[0].split(', ')
        comp_name = parts[0].split('= ')[1].strip()
        comp_ver = parts[1].split('= ')[1].strip()
        count = item[1]
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