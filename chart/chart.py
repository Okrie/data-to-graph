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
    
    # 현재 진행 중
    # 05.14 각 도표별 필요 인자 및 설정 할 수 있는 인자 값 초기화 및 정리, 설명 추가 진행 중
    # draw graph
    def drawGraph(self, graphType : str = None, graphStyle : plt.style.available = 'ggplot', **kwargs):
        """
        Draw a graph with specified parameters.

        Args:
            graph_type (str, optional): Type of the graph ('scatter', 'line', 'bar', etc.). Defaults to None.
            graph_style (str, optional): Style of the graph (see available styles below). Defaults to 'ggplot'.\n
            **kwargs:
                Markers:
                    ```'.' - point marker 
                    ',' - pixel marker 
                    'o' - circle marker 
                    'v' - triangle_down marker 
                    '^' - triangle_up marker 
                    '<' - triangle_left marker 
                    '>' - triangle_right marker 
                    '1' - tri_down marker 
                    '2' - tri_up marker 
                    '3' - tri_left marker 
                    '4' - tri_right marker 
                    '8' - octagon marker 
                    's' - square marker 
                    'p' - pentagon marker 
                    'P' - plus (filled) marker 
                    '*' - star marker 
                    'h' - hexagon1 marker 
                    'H' - hexagon2 marker 
                    '+' - plus marker 
                    'x' - x marker 
                    'X' - x (filled) marker 
                    'D' - diamond marker 
                    'd' - thin_diamond marker 
                    '|' - vline marker 
                    '_' - hline marker 
                    ```

                Line Styles:
                    ```'-'  - solid line style 
                    '--' - dashed line style 
                    '-.' - dash-dot line style 
                    ':'  - dotted line style 
                    ```

                Colors:
                    Single letter color codes ('b' for blue, 'r' for red, etc.) 
                    'CN' colors that index into the default property cycle 
                    Full names ('green', 'blue', etc.) 
                    Hex strings ('#008000', '#0000FF', etc.) 

        Returns:
            JSON => Graph PNG Image To Base64Encode String
        """

        
        # ARGS
        __GRAPH_TYPE: str = kwargs.pop('graphtype', None)
        __GRAPH_STYLE: plt.style.available = kwargs.pop('graphstyle', None)
        __XLABEL: str = kwargs.pop('xlabel', None)
        __YLABEL: str = kwargs.pop('ylabel', None)
        __COLOR: str | list = kwargs.pop('color', None)
        __WIDTH: int = kwargs.pop('width', None)
        __HEIGHT: int = kwargs.pop('height', None)
        
        
        plt.style.use(graphStyle)
        # print(f'self._data = \n{self._data}\n')
        
        # 원본 보존을 위한 copy
        data = self._data.copy()

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
