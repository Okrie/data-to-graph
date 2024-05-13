import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import json
from datetime import datetime

class drawChart():
    _data : pd.DataFrame = None
    
    def __init__(self):
        # self._data = self.loadJsonDataToDataframe(jsonData)
        # print(self._data)
        pass
        
        
    
    def seperateJSONResult(self, originJsonData = None):
        # __jsonType = type(json.loads(originJsonData)["result"])

        # 이 부분 다시 생각하기, 사이즈가 아닌 타입으로 구분하는 것이 더 나을듯
        __len = len(json.loads(originJsonData)["result"])
        print(f'__len = {__len}')
        
        if __len == 1:
            print(originJsonData)
            __jsondata = pd.read_json(originJsonData)["result"]
            __jsondata = __jsondata.to_frame().T
        else:
            __jsondata = pd.DataFrame.from_records(json.loads(originJsonData)['result'], index=None)
            # for i in range(__len):
            #     print(pd.DataFrame.from_records(json.loads(originJsonData)['result'], index='_time'))
            #     print(json.loads(originJsonData)["result"][i])
            #     tmp = pd.DataFrame().from_dict(json.loads(originJsonData)["result"][i])
            #     __jsondata = pd.concat([__jsondata, tmp])
            print(f'1 : \n{__jsondata}')
            for i in range(__len):
                print(f'11 : \n{__jsondata.iloc[i]}')
                # __jsondata.iloc[i] = datetime.fromisoformat(__jsondata.iloc[i][:-5]).strftime('%Y-%m-%d %H:%M:%S')
            # _convertTime = datetime.fromisoformat(__jsondata['_time'][:-5]).strftime('%Y-%m-%d %H:%M:%S')
            # print(_convertTime)
            # __jsondata['_time'] = _convertTime
            __jsondata = __jsondata.T

        print(f'2 : {__jsondata}')
        # _convertTime = datetime.fromisoformat(__jsondata['_time'][:-5]).strftime('%Y-%m-%d %H:%M:%S')
        # print(_convertTime)
        # __jsondata['_time'] = _convertTime

        # __jsondata = __jsondata.to_frame().T
        return __jsondata, __len


    def loadJsonDataToDataframe(self, jsondata: dict = None):
        __jsondata, __len = self.seperateJSONResult(jsondata)
        
        if __len > 1:
            print("Data iS LIST TYPE")
        else:
            print("Data iS DICT TYPE")
        
        print(f' __len = {__len}')
        
        df = pd.DataFrame()
            
        for i in range(__len):
            print(__jsondata)
            # _convertTime = datetime.fromisoformat(__jsondata['_time'].iloc[i][:-5]).strftime('%Y-%m-%d %H:%M:%S')
            # __jsondata['_time'].iloc[i] = _convertTime
        
        # for line in range(len(jsondata)):
        #     print(line)
        #     tmp = pd.read_json(jsondata[line])
        #     print(tmp)
        #     tmp = tmp.to_frame().T
            
        #     # type 정리
        #     # type object to datetime
        #     _convertTime = datetime.fromisoformat(tmp['_time'].iloc[0][:-5]).strftime('%Y-%m-%d %H:%M:%S')
        #     tmp['_time'] = _convertTime
            
        #     # type object to integer
        #     tmp = tmp.astype(dtype='int64', errors='ignore')
        #     df = pd.concat([df, tmp])
        
        # df.set_index('_time', inplace=True)
        
        return df
    
    def dfTypeChange(jsondata: dict = None):
        __jsondata = pd.read_json(jsondata)["result"]
        __jsondata = __jsondata.to_frame().T
            
        # type 정리
        # type object to datetime
        _convertTime = datetime.fromisoformat(__jsondata['_time'].iloc[0][:-5]).strftime('%Y-%m-%d %H:%M:%S')
        __jsondata['_time'] = _convertTime
        
        # type object to integer
        __jsondata = __jsondata.astype(dtype='int64', errors='ignore')
        
        return __jsondata
    
    
    # draw graph
    def drawGraph(self, graphType : str = None, graphStyle : plt.style.available = 'ggplot'):
        
        plt.style.use(graphStyle)
        data = self._data

        __graphToBytes = BytesIO()

        # Default Line Graph
        if graphType == None:
            dfGraph = data.T
            fig = plt.figure(figsize=(14, 5))
            
            ax = fig.add_subplot(1, 1, 1)
            
            plt.xlabel('Day')
            plt.ylabel("Count")
            plt.xticks(rotation = 45)
            
            for i in range(len(self._data.columns)):
                ax.plot(
                    dfGraph.columns,
                    dfGraph.loc[self._data.columns[i], :],
                    marker='o',
                    markersize=10,
                    lw=2,
                    label=f'{self._data.columns[i]}',
                )
            plt.legend(loc='best')
            
        # Line & Bar Graph
        elif graphType == 'twin':
            dfGraph = data.T
            
            # Bar Graph
            ax1 = data.plot(
                kind = 'bar',
                figsize=(12, 5),
                width = 0.7,
                stacked=True,
            )
            
            ax = ax1.twinx()
            
            plt.xlabel('Day')
            plt.ylabel("Count")
            plt.xticks(rotation = 45)
            
            # Line Graph
            for i in range(len(self._data.columns)):
                ax.plot(
                    dfGraph.columns,
                    dfGraph.loc[self._data.columns[i], :],
                    marker='o',
                    markersize=10,
                    lw=2,
                    label=f'{self._data.columns[i]}',
                )
            ax1.legend(loc='best')
        
        # Bar, Pie Graph
        else:
            # Bar Graph
            if graphType == 'bar':
                data.plot(
                    kind = graphType,
                    figsize=(12, 5),
                    width = 0.7,
                    stacked=True,
                )
                plt.legend(loc='best')
                
            # Pie Graph
            else:
                dfGraph = data
                dfGraph.loc['Total', :] = dfGraph[dfGraph.columns].sum(axis=0)
                dfGraph = dfGraph.T
                dfGraph.drop('NULL', axis=0, inplace=True)
                
                dfGraph['Total'].plot(
                    kind='pie',
                    figsize=(20, 12),
                    autopct='%.2f%%',    # %% : % 출력
                    startangle=10,
                )
                plt.xlabel(f'{dfGraph.columns[0]} ~ {dfGraph.columns[-2]} Status Pie Chart')
                plt.legend(labels = data.columns, loc='best')
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=100, bbox_inches='tight')
        plt.close()
        import base64
        
        # Base64 encoding
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,%s" % __convBase64        
