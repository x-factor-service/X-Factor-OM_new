from common.dataFrame import dataFrame
#print(dataFrame())

# 대시보드 상단 디스크 사용률 초과 서버, 메모리 사용률 초과 서버, 씨피유 사용률 초과 서버
def transform_donutData(sensorName) :
    data = dataFrame()[dataFrame()[sensorName].str.upper() == 'YES']
    transformDonutData = len(data)
    return transformDonutData

# 대시보드 상단 OS 설치현황, 유/무선 연결 현황, 물리/가상 자산 현황(전처리 포함)
def transform_pieData(sensorName):
    valueCounts = dataFrame()[sensorName].value_counts()
    values = []
    counts = []
    preprocessing_list = ['no result']
    for value, count in zip(valueCounts.index, valueCounts.values):
        if not any(excluded_value.upper() in value.upper() for excluded_value in preprocessing_list):
            values.append(value)
            counts.append(count)
    transformPieData = {'name': values, 'value': counts}
    return transformPieData
