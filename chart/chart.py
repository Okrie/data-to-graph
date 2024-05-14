import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO, StringIO
import json
from datetime import datetime

class drawChart():
    _data : pd.DataFrame = None
    
    def __init__(self):
        # print(self._data)
        pass
    
    # 받은 데이터가 한개, 한개 이상일 때로 구분하여 DataFrame 형태로 변경
    def seperateJSONResult(self, originJsonData = None):
        __jsonType = type(json.loads(originJsonData)["result"])
        
        # Result 데이터가 1개 일때
        if __jsonType == dict:
            __jsondata = pd.read_json(StringIO(originJsonData))["result"]
            __jsondata = __jsondata.to_frame().T
            
        # Result 데이터가 1개 이상 일 때
        else:
            __jsondata = pd.DataFrame.from_records(json.loads(originJsonData)['result'])

        __jsondata.reset_index(drop=True, inplace=True)
        
        __jsondata.set_index('_time', inplace=True)
        
        return __jsondata, len(__jsondata)


    # Graph를 그리기 위한 Data 정제 과정
    # 데이터를 받아 하나의 DataFrame으로 병합
    def loadJsonDataToDataframe(self, jsondata: dict = None):
        __jsondata, __len = self.seperateJSONResult(jsondata)
        
        # print(f' __len = {__len}')
        # if __len > 1:
        #     print("Data iS LIST TYPE")
        # else:
        #     print("Data iS DICT TYPE")
        
        # type object to integer
        __jsondata = __jsondata.astype(dtype='int64', errors='ignore')
        
        # type object to datetime
        # __jsondata._time = __jsondata._time.apply(self.tranform_datetype)
        
        self._data = pd.concat([self._data, __jsondata])

        return self._data
    
    
    # 현재 일부 문제가 있어 미사용
    # 시간 값을 년-월-일 시:분:초로 변경하는 과정
    @staticmethod
    def tranform_datetype(beforeDatetime):        
        return datetime.fromisoformat(beforeDatetime[:-5]).strftime('%Y-%m-%d %H:%M:%S')
    
    
    # draw graph
    def drawGraph(self, graphType : str = None, graphStyle : plt.style.available = 'ggplot'):
        
        plt.style.use(graphStyle)
        print(f'self._data = \n{self._data}\n')
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
