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
                GraphStyle:
                    ```
                    'line'   - default Graph
                    'bar'    - bar Graph
                    'pie'    - pie Graph
                    ```
                    
                Markers:
                    ```
                    '.' - point marker 
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
                    ```
                    '-'  - solid line style 
                    '--' - dashed line style 
                    '-.' - dash-dot line style 
                    ':'  - dotted line style 
                    ```

                Colors:
                    ```
                    Can Using Colors 
                        - 'b', 'g', 'c', 'k', 'm', 'w', 'r', 'y' 
                        - Tableau Colors
                        - CSS Colors
                        - Hex String
                    
                    Single letter color codes ('b' for blue, 'r' for red, etc.) 
                    'CN' colors that index into the default property cycle 
                    Full names ('green', 'blue', etc.) 
                    Hex strings ('#008000', '#0000FF', etc.)
                    ``` 
                    
                Legend:
                    ```
                    'best'   - auto, default
                    'upper right'   - upper right
                    'upper center'  - upper center
                    'upper left'    - upper left
                    'lower right'   - lower right
                    'lower center'  - lower center
                    'lower left'    - lower left
                    'right'         - right
                    'center'        - center
                    'left'          - left
                    ```

        Returns:
            JSON => Graph PNG Image To Base64Encode String
        """

        # Data ARGS
        __DROPCOLUMN: bool = kwargs.pop('drop', False)
        __DROPCOLUMNS: list[str] = kwargs.pop('dropcolumn', None)
        
        # Common GRAPH ARGS
        __GRAPH_STYLE: plt.style.available = kwargs.pop('graphstyle', 'ggplot')
        __GRAPH_TYPE: str = kwargs.pop('kind', 'line')
        
        ## GRAPH SIZE
        __FIGSIZE: tuple[int, int] = kwargs.pop('figsize', (12, 5))
        
        ## GRAPH View Settings
        ### GRAPH TEXT
        __TITLE: str = kwargs.pop('title', None)
        __LABEL: str = kwargs.pop('label', None)
        __XLABEL: str = kwargs.pop('xlabel', None)
        __YLABEL: str = kwargs.pop('ylabel', None)
        
        ### GRAPH X, Y Limit Length, Height
        __XLIM: list[float, float] = kwargs.pop('xlim', None)
        __YLIM: list[float, float] = kwargs.pop('ylim', None)
        
        ### COLOR, WIDTH, HEIGHT, GRID, AXIS
        __COLOR: str | list = kwargs.pop('color', None)
        __GRID: bool = kwargs.pop('grid', True)
        __AXIS: int = kwargs.pop('axis', 0)
        
        ## GRAPH layout margin
        __TIGHTLAYOUT: bool = kwargs.pop('tightlayout', False)
        
        ## LABEL TEXT ROTATE
        __XTICKS: float = kwargs.pop('xticks', 0)
        __YTICKS: float = kwargs.pop('yticks', 0)
        
        ## LEGEND ARGS
        __LEGENDPOS: str = kwargs.pop('legendpos', 'best')
        __LEGENDFONTSIZE: int = kwargs.pop('legendfontsize', 7)
        
        
        # Line GRAPH ARGS
        __MARKER: str = kwargs.pop('marker', '.')
        __MARKERSIZE: int = kwargs.pop('markersize', 5)
        
        # Bar GRAPH ARGS
        __WIDTH: float = kwargs.pop('width', 0.7)
        __LINEWIDTH: int = kwargs.pop('linewidth', 1)
        __STACKED: bool = kwargs.pop('stacked', False)
        
        # Line with Bar GRAPH ARGS
        __TWINX: bool = kwargs.pop('twinx', False)
        __TWINY: bool = kwargs.pop('twiny', False)
        
        # Pie GRAPH ARGS
        __AUTOPCT: str = kwargs.pop('autopct', '%.2f%%')    # %% : % 출력
        __STARTANGLE: float = kwargs.pop('startangle', 10)
        
        
        plt.style.use(__GRAPH_STYLE)
        # print(f'self._data = \n{self._data}\n')
        
        # 원본 보존을 위한 copy
        data = self._data.copy()

        __graphToBytes = BytesIO()
        
        plt.title(__TITLE)
        

        # Default Line Graph
        if graphType == None:
            dfGraph = data.T
            fig = plt.figure(figsize=__FIGSIZE)
            
            ax = fig.add_subplot(1, 1, 1)
            
            plt.xlabel(__XLABEL)
            plt.ylabel(__YLABEL)
            plt.xticks(rotation = __XTICKS)
            plt.yticks(rotation = __YTICKS)
            
            for i in range(len(self._data.columns)):
                ax.plot(
                    dfGraph.columns,
                    dfGraph.loc[self._data.columns[i], :],
                    marker= __MARKER,
                    markersize= __MARKERSIZE,
                    lw= __LINEWIDTH,
                    label= __LABEL,
                )
                
            plt.legend(loc=__LEGENDPOS, fontsize=__LEGENDFONTSIZE)
            
        # Line & Bar Graph
        elif graphType == 'twin':
            dfGraph = data.T
            
            # Bar Graph
            ax1 = data.plot(
                kind = __GRAPH_TYPE,
                figsize= __FIGSIZE,
                width = __WIDTH,
                stacked= __STACKED,
            )
            
            if __TWINX | __TWINY:
                if __TWINX:
                    ax = ax1.twinx()
                elif __TWINY:
                    ax = ax1.twiny()
            
            plt.xlabel(__XLABEL)
            plt.ylabel(__YLABEL)
            plt.xticks(rotation = __XTICKS)
            plt.yticks(rotation = __YTICKS)
            
            # Line Graph
            for i in range(len(self._data.columns)):
                ax.plot(
                    dfGraph.columns,
                    dfGraph.loc[self._data.columns[i], :],
                    marker= __MARKER,
                    markersize= __MARKERSIZE,
                    lw= __LINEWIDTH,
                    label= __LABEL,
                )
            ax1.legend(loc= __LEGENDPOS)
        
        # Bar, Pie Graph
        else:
            # Bar Graph
            if graphType == 'bar':
                data.plot(
                    kind = __GRAPH_TYPE,
                    figsize= __FIGSIZE,
                    width = __WIDTH,
                    stacked= __STACKED,
                )
                plt.legend(loc= __LEGENDPOS)
                
            # Pie Graph
            else:
                dfGraph = data
                dfGraph.loc['Total', :] = dfGraph[dfGraph.columns].sum(axis=0)
                dfGraph = dfGraph.T
                
                if __DROPCOLUMN:
                    dfGraph.drop(__DROPCOLUMNS, axis=0, inplace=True)
                
                dfGraph['Total'].plot(
                    kind= __GRAPH_TYPE,
                    figsize= __FIGSIZE,
                    autopct= __AUTOPCT,
                    startangle= __STARTANGLE,
                    grid= __GRID,
                )
                plt.xlabel(__XLABEL)
                plt.legend(labels = data.columns, loc= __LEGENDPOS, fontsize= __LEGENDFONTSIZE)
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=100, bbox_inches='tight')
        plt.close()
        import base64
        
        # Base64 encoding
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,%s" % __convBase64
