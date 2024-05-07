import os
import pandas as pd
from io import BytesIO
from datetime import datetime



def loadJsonData(fileName: str = ''):
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
