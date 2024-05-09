import os
import pandas as pd
import json
from io import BytesIO
from datetime import datetime



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
    