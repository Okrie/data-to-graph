import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO, StringIO
import json
from datetime import datetime

class drawChart:
    _data: pd.DataFrame = None
    _len: int = 0
    
    # OPTIONS
    general: dict = {
        # Common GRAPH ARGS
        'graph_style': 'ggplot',    # graph view style
        
        ## GRAPH SIZE
        'fig_size': (12, 5),    # graph size        tuple
        
        ## GRAPH View Settings
        ### GRAPH TEXT
        'title': None,          # graph title                   str
        'label': _data.columns if _data != None else None, # legend label                  list | series
        
        # Flip x - y
        'flip': False,          # Flip X-Y axis                 True, False
    }
    
    x_axis: dict = {
        'label': None,          # x axis label                  str
        'ticks': 45,            # x label text rotate degree    -90 ~ 90
        'min' : 0,              # limit low value
        'max' : 1000,           # limit high value
    }
    
    y_axis: dict = {
        'label': None,          # y axis label                  str
        'ticks': 0,             # y label text rotate degree    -90 ~ 90
        'min' : 0,              # limit low value
        'max' : 1000,           # limit high value
    }
    
    legend: dict = {
        'location': 'best',     # legend location               best, left, center, right, upper [left, center, right], lower [left, center, right]
        'fontsize': 7,          # legend fontsize               int
    }
    
    overlay: dict = {
        ### COLOR, WIDTH, HEIGHT, GRID, AXIS
        'color': None,          # graph value color             str | list
        'grid': True,           # graph in grid background      True, False
        'axis': 0,              # value axis                    0 - horizental, 1 - vertical
        
        ## GRAPH layout margin
        'tight_layout': False,  # graph layout margin           True, False
        
        # Marker
        'marker': 'o',          # draw line on marker           
        'marker_size': 5,       # marker size
    }
    
    def __init__(self):
        # print(self._data)
        pass
    
    # 받은 데이터가 한개, 한개 이상일 때로 구분하여 DataFrame 형태로 변경
    def seperateJSONResult(self, originJsonData = None, index_column = '_time'):
        __jsonType = type(json.loads(originJsonData)["result"])
        
        # Result 데이터가 1개 일때
        if __jsonType == dict:
            __jsondata = pd.read_json(StringIO(originJsonData))["result"]
            __jsondata = __jsondata.to_frame().T
            
        # Result 데이터가 1개 이상 일 때
        else:
            __jsondata = pd.DataFrame.from_records(json.loads(originJsonData)['result'])

        __jsondata.reset_index(drop=True, inplace=True)
        
        # index로 지정할 컬럼 유무 체크
        try:
            __jsondata.set_index(index_column, inplace=True)
        except:
            print(__jsondata)
            raise print("Not Exist column for using index \n Check Columns")
            
        
        self._len = len(__jsondata)
        
        return __jsondata


    # Graph를 그리기 위한 Data 정제 과정
    # 데이터를 받아 하나의 DataFrame으로 병합
    def loadJsonDataToDataframe(self, jsondata: dict = None):
        __jsondata = self.seperateJSONResult(jsondata)
        
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
    
    # option 정의 재사용을 위한 함수
    def optionUpdate(self, **kwargs):
        self.general.update(kwargs.pop('general', self.general))
        self.x_axis.update(kwargs.pop('x_axis', self.x_axis))
        self.y_axis.update(kwargs.pop('y_axis', self.y_axis))
        self.legend.update(kwargs.pop('legend', self.legend))
        self.overlay.update(kwargs.pop('overlay', self.overlay))
    
    # 05.17 그래프 분리
    # Line Graph
    def line(self, general: dict, x_axis: dict, y_axis: dict, legend: dict, overlay: dict):
        self.optionUpdate(general, x_axis, y_axis, legend, overlay)
        
        
        return
    
    # 현재 진행 중
    # 05.14 각 도표별 필요 인자 및 설정 할 수 있는 인자 값 초기화 및 정리, 설명 추가 진행 중
    # draw graph
    def drawGraph(self, graphStyle : plt.style.available = 'ggplot', **kwargs):
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
        __XTICKS: int = kwargs.pop('xticks', 45)
        __YTICKS: int = kwargs.pop('yticks', 0)
        
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
        
        if __DROPCOLUMNS != None:
            data.T.drop(__DROPCOLUMNS, axis=0, inplace=True)
            print(data)
            
        # Line, Pie Graph는 T
        # Bar Graph는 원본

        # Default Line Graph
        if __GRAPH_TYPE == 'line':
            dfGraph = data.T.copy()
            fig = plt.figure(figsize=__FIGSIZE)
            
            ax = fig.add_subplot(1, 1, 1)
            
            print(dfGraph.T)
            
            for i in range(len(self._data.columns)):
                ax.plot(
                    dfGraph.columns,
                    dfGraph.loc[self._data.columns[i], :],
                    marker= __MARKER,
                    markersize= __MARKERSIZE,
                    lw= __LINEWIDTH,
                )
            
            plt.title(__TITLE, loc='center')
            plt.xlabel(__XLABEL)
            plt.ylabel(__YLABEL)
            plt.xticks(rotation = __XTICKS)
            plt.yticks(rotation = __YTICKS)
            plt.legend(labels = self._data.columns, loc=__LEGENDPOS, fontsize=__LEGENDFONTSIZE)
        
        # Line & Bar Graph
        elif __GRAPH_TYPE == 'twin':
            dfGraph = data.T.copy()
            
            # Bar Graph
            ax1 = data.plot(
                kind = 'bar',
                figsize= __FIGSIZE,
                width = __WIDTH,
                stacked= __STACKED,
                xlabel= __XLABEL,
                ylabel= __YLABEL,
                xlim= __XLIM,
                ylim= __YLIM,                
            )
            
            if __TWINX | __TWINY:
                if __TWINX:
                    ax = ax1.twinx()
                elif __TWINY:
                    ax = ax1.twiny()
            
            # Line Graph
            for i in range(len(data.columns)):
                ax.plot(
                    dfGraph.columns,
                    dfGraph.loc[data.columns[i], :],
                    marker= __MARKER,
                    markersize= __MARKERSIZE,
                    lw= __LINEWIDTH,
                )

            plt.title(__TITLE, loc='center')
            plt.xlabel(__XLABEL)
            plt.ylabel(__YLABEL)
            plt.xticks(rotation = __XTICKS)
            plt.yticks(rotation = __YTICKS)

            ax1.legend(labels = self._data.columns, loc= __LEGENDPOS)

        # Bar, Pie Graph
        else:
            # Bar Graph
            if __GRAPH_TYPE == 'bar':
                dfGraph = data.copy()
                
                dfGraph.plot(
                    kind = __GRAPH_TYPE,
                    figsize= __FIGSIZE,
                    width = __WIDTH,
                    stacked= __STACKED,
                )
                
                plt.title(__TITLE, loc='center')
                plt.xlabel(__XLABEL)
                plt.ylabel(__YLABEL)
                plt.xticks(rotation = __XTICKS)
                plt.yticks(rotation = __YTICKS)
                plt.legend(loc= __LEGENDPOS)
                
            # Pie Graph
            else:
                dfGraph = data.copy()
                dfGraph.loc['Total', :] = dfGraph[dfGraph.columns].sum(axis=0)
                dfGraph = dfGraph.T
                
                dfGraph['Total'].plot(
                    kind= 'pie',
                    figsize= __FIGSIZE,
                    autopct= __AUTOPCT,
                    startangle= __STARTANGLE,
                    grid= __GRID,
                    
                )
                
                plt.title(__TITLE, loc='center')
                plt.xlabel(__XLABEL)
                plt.ylabel(__YLABEL)
                plt.xticks(rotation = __XTICKS)
                plt.yticks(rotation = __YTICKS)

                plt.legend(labels = self._data.columns, loc= __LEGENDPOS, fontsize= __LEGENDFONTSIZE)
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=200, bbox_inches='tight')
        plt.close()
        
        # Base64 encoding
        import base64
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,%s" % __convBase64
