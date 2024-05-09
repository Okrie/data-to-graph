import os
import pandas as pd
import json
from io import BytesIO
from datetime import datetime
import re


# get regexr pattern
def getPattern(type: str = None):
    pattern = ""
    type = type.lower()
    
    if type == "ip":
        pattern = "\\b^(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\\.){3}(?:(?:2([0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\\b"
    elif type == "date":
        pattern = "\\b(?:\\d{2}/\\w{3}/\\d{4}:\\d{2}:\\d{2}:\\d{2})\\b"
    elif type == "method":
        pattern = "\\b(?:GET|POST|PUT|DELETE)\\b"
    elif type == "endpoint":
        pattern = "\\b(?:\\s[^\"](.\\w+.\\w+).\w{1,}\\?)\\b"
    elif type == "status":
        pattern = "\\b[\"](?:[^\\.]?\\d{3})\\b"

    return pattern

# data to json
def seperateData(data: str = None):
    ip = re.findall(getPattern("IP"), data)
    _time = re.findall(getPattern("DATE"), data)
    method = re.findall(getPattern("METHOD"), data)
    status = str(re.findall(getPattern("STATUS"), data)[0])[2:] \
        if len(re.findall(getPattern("STATUS"), data)) > 0 else str(re.findall(getPattern("STATUS"), data))[2:],

    return {\
        "ip" : ip,
        "_time" : _time,
        "method" : method,
        "status" : status,
    }

# read log data
def readLogData(fileName: str = None):
    with open(f"{os.path.realpath('.')}/static/data/{fileName}", "r") as f:
        data = []
        for line in f:
            data.append(seperateData(line))

    return data



##########################################
###########        GRAPH       ###########
##########################################
def loadJsonDataForGraph(fileName: str = ''):
    df = pd.DataFrame()
    
    with open(f"{os.path.realpath('.')}/static/data/{fileName}.json", "rb") as f:
        for line in f:
            tmp = pd.read_json(BytesIO(line))
            tmp = tmp['result'].to_frame().T
            
            # type 정리
            # type object to datetime
            _convertTime = datetime.fromisoformat(tmp['_time'].iloc[0][:-5]).strftime('%Y-%m-%d %H:%M:%S')
            tmp['_time'] = _convertTime
            
            # type object to integer
            tmp = tmp.astype(dtype='int64', errors='ignore')
            df = pd.concat([df, tmp])
    
    df.set_index('_time', inplace=True)
    
    return df

def loadJsonDataForSpreadSheet(fileName: str = ''):
    
    with open(f"{os.path.realpath('.')}/static/data/{fileName}.json", "r") as f:
        data = []
        for line in f:
            tmp = json.loads(line)["result"]
            tmplist = [i for i in tmp]
            data.append(tmplist)
            
    return data
    