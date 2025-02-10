# coding=utf-8
"""
    Data To Graph
    Author: Okrie
"""

import matplotlib.pyplot as plt
import dateutil.parser
import numpy as np
from io import BytesIO

# 한글 폰트 설정
import matplotlib.font_manager as fm
plt.rcParams['axes.unicode_minus'] = False
fe = fm.FontEntry(fname=r'/usr/share/fonts/truetype/nanum/NanumGothic.ttf', name='NanumGothic')
fm.fontManager.ttflist.insert(0, fe)
plt.rcParams.update({'font.size': 10, 'font.family': 'NanumGothic'})
# 한글 폰트 설정 끝

# prevent scientific notation
plt.ticklabel_format(style='plain', axis='y')

class drawChart:
    """
        ## Data To Graph
        - loadJsonDataToDataframe 로 데이터를 넣어 각 line, bar, twin, pie 함수를 사용하여 base64 인코딩 된 문자열을 받는다.
        
        ### Args:
            loadJsonDataToDataframe: 이 함수로 Jsondata를 인자로 넣어 지정
            line: 선그래프
            bar: 막대형 그래프
            twin: 선, 막대 혼합 그래프
            pie: 원 그래프

        ### Returns:
            - Web에서 사용하기 위한 Graph PNG를 Base64로 인코딩해 Return
    """
    
    _data: list = []
    # _data: pd.DataFrame = None
    _len: int = 0
    
    
    __SPLUNK_BASE_COLOR_MAP = {
        'base': [
            '#7B5547',
            '#77D6D8',
            '#4A7F2C',
            '#F589AD',
            '#6A2C5D',
            '#AAABAE',
            '#9A7438',
            '#A4D563',
            '#7672A4',
            '#184B81'
        ],
        'categorical_1': [
            '#006D9C',
            '#4FA484',
            '#EC9960',
            '#AF575A',
            '#B6C75A',
            '#62B3B2',
            '#294E70',
            '#738795',
            '#EDD051',
            '#BD9872'
        ],
        'categorical_2': [
            '#5A4575',
            '#7EA77B',
            '#708794',
            '#D7C6B0',
            '#339BB2',
            '#55672D',
            '#E6E1A0',
            '#96907F',
            '#87BC65',
            '#CF7E60'
        ],
        'categorical_3': [
            '#7B5547',
            '#77D6D8',
            '#4A7F2C',
            '#F589AD',
            '#6A2C5D',
            '#AAABAE',
            '#9A7438',
            '#A4D563',
            '#7672A4',
            '#184B81'
        ]
    }
    
    # OPTIONS
    DEFAULT_OPTION: dict = {
        'general': {
            # Common GRAPH ARGS
            'graph_style': 'ggplot',    # graph view style
            
            ## GRAPH SIZE
            'fig_size': (8, 5),    # graph size        tuple
            
            ## GRAPH View Settings
            ### GRAPH TEXT
            'title': None,          # graph title                   str
            'label': None,          # legend label                  list | series
            
            # Flip x - y
            'flip': False,          # Flip X-Y axis                 True, False
            
            # DropColumns
            'drop_columns': False,  # Drop Column on Graph          True, False
            'drop_columns_name': [''], # Drop Column Name           list[str]
            'drop_column_axis': 1,  # Drop Column Axis              0 - horizental, 1 - vertical
            
            # Graph resolution
            'dpi': 150,             # Graph Resolution              default 150
            'img_width': 700,       # Image px                      default 700
            
            # View Max Value Text
            'value_text': False,    # View Max Value Text           default False
        },
        'x_axis': {
            'label': None,          # x axis label                  str
            'labelsize': 12,        # x label fontsize              default 12
            'fontsize': 7,          # x label fontsize              default 7
            'ticks': 45,            # x label text rotate degree    -90 ~ 90
            'min' : None,           # limit low value
            'max' : None,           # limit high value
        },
        'y_axis': {
            'label': None,          # y axis label                  str
            'labelsize': 12,        # x label fontsize              default 12
            'fontsize': 5,          # y label fontsize              default 5
            'ticks': 0,             # y label text rotate degree    -90 ~ 90
            'min' : None,           # limit low value
            'max' : None,           # limit high value
        },
        'overlay': {
            ### GRID, Legend
            'grid': True,           # graph in grid background      True, False
            'legend': True,         # graph on legend On / Off      True, False
        },
        'legend': {
            'title': None,          # legend title                  str
            'labels': None,         # legend label                  columns
            'location': 'upper left',     # legend location               best, left, center, right, upper [left, center, right], lower [left, center, right]
            'fontsize': 5,          # legend fontsize               int
        },
        'line': {
            'width': 1,             # Line Width                    float over 0
            'style': '-',           # Line Style                    default = '-', '--' '-.' ':'
            'colors': __SPLUNK_BASE_COLOR_MAP['base'], # Line Colors    default on SPLUNK color map
            # Marker
            'marker': None,         # draw line on marker
            'marker_size': 5,       # marker size
        },
        'bar': {
            'width': 0.8,             # Bar Width                     float over 0
            'colors': __SPLUNK_BASE_COLOR_MAP['categorical_2'], # Bar Colors    default on SPLUNK color map
            'stack': True,          # Bar values Stacked            True, False
            'align': 'center',          # Bar align                     center, edge
        },
        'twin': {
            'twin': 'x',            # Twin Axis                     default x  y
            'x_label': '',          # Twin x label                  str
            'y_label': '',          # Twin y label                  str
            'x_min': 0,          # Twin x min value              float
            'x_max': None,          # Twin x max value              float
            'y_min': 0,          # Twin y min value              float
            'y_max': None,          # Twin y max value              float
            'legend': 'upper right',# Second Legend location        default 'upper left'
            'legend_fontsize': 7,   # legend fontsize               int
            'tight_layout': False,  # graph to graph layout margin  True, False
        },
        'pie': {
            'autopct': '%.2f%%',    # display percentage            default %.2f%%
            'labeldistance': 1.1,   # label <-> pie distance        default 1.1  float
            'startangle': 0,        # Start point angle             default 0
            'shadow': False,        # Shadow On / Off               True, False
            'radius': 1,            # Pie Radius                    float
            'colors': __SPLUNK_BASE_COLOR_MAP['categorical_3'], # Pie Colors    default on SPLUNK color map
            'wedge_width': None,    # Pie To Donut width            float
            'wedge_edge_color': None,# Pie To Donut color           default following matplotlib colors 
            'explode': None,        # Pie piece Explode             tuple[float]     **tuple len == explode len**
            'arrow': True,         # Arrow option on / off         True, False
        },
    }
    
    def __init__(self):
        self._data = []
        pass
    
    # 받은 데이터가 한개, 한개 이상일 때로 구분하여 dict(key: value(list)) 형태로 변경
    def seperateJSONResult_json(self, originJsonData = None):
        result_data = originJsonData
        
        if isinstance(result_data, dict):
            json_data = [result_data]
        else:
            json_data = result_data
        
        for item in json_data:
            for key, value in item.items():
                if value == '':
                    item[key] = None
        
        self._len = len(json_data)
        return json_data

    # Graph를 그리기 위한 Data 정제 과정
    def loadJsonDataToDict(self, jsondata: dict = None, delReservedWord: bool = True):
        json_data = self.seperateJSONResult_json(jsondata)
        
        self._data.extend(json_data)

        # 예약어 삭제 '_span', '_spandays'
        if delReservedWord:
            columns = ['_span', '_spandays']
            for col in columns:
                for item in self._data:
                    if col in item:
                        del item[col]

        return self._data
    
    # 시간 값을 년-월-일 시:분:초로 변경하는 함수
    @staticmethod
    def transformDatetype(beforeDatetime):
        return dateutil.parser.parse(beforeDatetime).strftime('%Y-%m-%d %H:%M:%S')
    
    # 빈 옵션에 Default 옵션을 지정하기 위한 함수
    def optionUpdate(self, defaultOption, overridesOption):
        if overridesOption != None:
            for k, v in overridesOption.items():
                if isinstance(v, dict) and k in defaultOption:
                    defaultOption[k] = self.optionUpdate(defaultOption.get(k, {}), v)
                else:
                    defaultOption[k] = v
        else:
            return self.DEFAULT_OPTION
        return defaultOption
    
    # 05.17 그래프 분리
    # Line Graph
    def line(self, option = dict):
        """## Line Graph

        ### Args:
            general (dict): 
                ```
                'general': {
                    'graph_style': 'ggplot', # graph view style
                    'fig_size': (12, 5), # graph size  tuple
                    'title': None, # graph title  str
                    'label': _data.columns if _data != None else None, # legend label  list | series
                    'flip': False, # Flip X-Y axis  True, False
                    'drop_columns': False, # Drop Column on Graph  True, False
                    'drop_columns_name': [''], # Drop Column Name  list[str]
                    'drop_column_axis': 0, # Drop Column Axis  0 - horizental, 1 - vertical
                    'dpi': 150, # Graph Resolution  default 150
                    'img_width': 700, # Image px  default 700
                    'value_text': False, # View Max Value Text  default False
                }
                ```
            x_axis (dict): 
                ```
                'x_axis': {
                    'label': None, # x axis label  str
                    'labelsize': 12, # x label fontsize  default 12
                    'fontsize': 7, # x label fontsize  default 7
                    'ticks': 45, # x label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            y_axis (dict):
                ```
                'y_axis': {
                    'label': None, # y axis label  str
                    'labelsize': 12, # y label fontsize  default 12
                    'fontsize': 5, # y label fontsize  default 5
                    'ticks': 0, # y label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            overlay (dict): 
                ```
                'overlay': {
                    'grid': True, # graph in grid background  True, False
                    'legend': True, # graph on legend On / Off  True, False
                }
                ```
            legend (dict): 
                ```
                'legend': {
                    'title': None, # legend title  str
                    'labels': None, # legend label  columns
                    'location': ''upper left', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
                    'fontsize': 7, # legend fontsize  int
                }
                ```
            line (dict):
                ```
                'line': {
                    'width': 1, # Line Width  float over 0
                    'style': '-', # Line Style  default = '-', '--' '-.' ':'
                    'colors': __SPLUNK_BASE_COLOR_MAP['base'], # Bar Colors  default on SPLUNK color map
                    'marker': 'o', # draw line on marker           
                    'marker_size': 5, # marker size
                }
                ```
        """
        updatedOption = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)

        general = updatedOption['general']
        x_axis = updatedOption['x_axis']
        y_axis = updatedOption['y_axis']
        legend = updatedOption['legend']
        overlay = updatedOption['overlay']
        line = updatedOption['line']
        
        plt.style.use(general['graph_style'])
        
        # 원본 보존을 위한 copy
        data = self._data.copy()
        
        # column 삭제 유무
        if general['drop_columns']:
            for col in general['drop_columns_name']:
                for item in data:
                    if col in item:
                        del item[col]
        
        # base64 Encoding을 위한 bytesIO
        __graphToBytes = BytesIO()

        # Draw Graph
        dfGraph = {key: [d[key] for d in data if key in d] for key in data[0].keys()}
        _, ax = plt.subplots(figsize=general['fig_size'])
        
        # prevent scientific notation
        plt.ticklabel_format(style='plain', axis='y')
        
        # Graph legend label
        label_x = list(dfGraph.keys())
        
        # x datas
        try:
            x = [self.transformDatetype(index) for index in dfGraph.get(list(dfGraph.keys())[0])]
            x_data = [self.transformDatetype(x) for x in dfGraph[label_x[0]]]
        except TypeError:
            x = [index for index in dfGraph.get(list(dfGraph.keys())[0])]
            x_data = [x for x in dfGraph[label_x[0]]]

        for i in range(1, len(label_x)):
            # y axis data
            y_data = [float(y) for y in dfGraph[label_x[i-1 if i == len(label_x) else i]]]
            ax.plot(
                x_data if (x_data != [None]) and (x_data != None) else label_x[0],
                y_data,
                marker= line['marker'],
                markersize= line['marker_size'],
                lw= line['width'],
                color=line['colors'][i % len(line['colors'])]
            )
            
            # View Max Value Text
            if general['value_text']:
                max_y = np.max(y_data)
                max_x = y_data.index(max_y)
                ax.text(max_x-0.25, max_y, f'{max_y}', ha='left', va='top')
        
        plt.title(general['title'], loc='center')
        plt.xlim((x_axis['min'], x_axis['max']))
        plt.ylim((y_axis['min'], y_axis['max']))
        plt.xlabel(x_axis['label'], fontsize=x_axis['labelsize'])
        plt.ylabel(y_axis['label'], fontsize=y_axis['labelsize'])
        plt.xticks(rotation = x_axis['ticks'], fontsize=x_axis['fontsize'])
        # 표현해야 될 데이터 많을 시 x 축 값 정리
        if len(x) > 10:
            ax.set_xticks(range(0, len(x), round(10 % len(x))))
            
        plt.yticks(rotation = y_axis['ticks'], fontsize=y_axis['fontsize'])
        plt.grid(visible=overlay['grid'])
        
        # legend on/off
        if overlay['legend']:
            plt.legend(title= legend['title'], labels = label_x[1:] if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=general['dpi'], bbox_inches='tight')
        plt.close()
        
        # Base64 encoding
        import base64
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return f'data:image/png;base64,{__convBase64}" width="{general["img_width"]}px"'
    
    
    # 05.20 그래프 분리
    # Bar Graph
    def bar(self, option = dict):
        """## Bar Graph

        ### Args:
            general (dict): 
                ```
                'general': {
                    'graph_style': 'ggplot', # graph view style
                    'fig_size': (12, 5), # graph size  tuple
                    'title': None, # graph title  str
                    'label': _data.columns if _data != None else None, # legend label  list | series
                    'flip': False, # Flip X-Y axis  True, False
                    'drop_columns': False, # Drop Column on Graph  True, False
                    'drop_columns_name': [''], # Drop Column Name  list[str]
                    'drop_column_axis': 0, # Drop Column Axis  0 - horizental, 1 - vertical
                    'dpi': 150, # Graph Resolution  default = 150
                    'img_width': 700 # Image px  default = 700
                }
                ```
            x_axis (dict): 
                ```
                'x_axis': {
                    'label': None, # x axis label  str
                    'labelsize': 12, # x label fontsize  default 12
                    'fontsize': 7, # x label fontsize  default 7
                    'ticks': 45, # x label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            y_axis (dict):
                ```
                'y_axis': {
                    'label': None, # y axis label  str
                    'labelsize': 12, # y label fontsize  default 12
                    'fontsize': 5, # y label fontsize  default 5
                    'ticks': 0, # y label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            overlay (dict): 
                ```
                'overlay': {
                    'grid': True, # graph in grid background  True, False
                    'legend': True, # graph on legend On / Off  True, False
                }
                ```
            legend (dict): 
                ```
                'legend': {
                    'title': None, # legend title  str
                    'labels': None, # legend label  columns
                    'location': 'best', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
                    'fontsize': 7, # legend fontsize  int
                }
                ```
            bar (dict):
                ```
                'bar': {
                    'width': 0.8, # Bar Width  float over 0
                    'colors': __SPLUNK_BASE_COLOR_MAP['categorical_2'], # Bar Colors  default on SPLUNK color map
                    'stack': True, # Bar values Stacked  True, False
                    'align': 'center', # Bar align  default center, edge
                }
                ```
        """
        updatedOption = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
        general = updatedOption['general']
        x_axis = updatedOption['x_axis']
        y_axis = updatedOption['y_axis']
        legend = updatedOption['legend']
        overlay = updatedOption['overlay']
        bar = updatedOption['bar']
        
        plt.style.use(general['graph_style'])
        
        # 원본 보존을 위한 copy
        data = self._data.copy()
        
        # column 삭제 유무
        if general['drop_columns']:
            for col in general['drop_columns_name']:
                for item in data:
                    if col in item:
                        del item[col]
        
        # base64 Encoding을 위한 bytesIO
        __graphToBytes = BytesIO()

        # Draw Graph
        dfGraph = {key: [d[key] for d in data if key in d] for key in data[0].keys()}
        _, ax = plt.subplots(figsize=general['fig_size'])
        
        # prevent scientific notation
        plt.ticklabel_format(style='plain', axis='y')
        
        # Graph legend label
        label_x = list(dfGraph.keys())
        
        # x datas
        try:
            x = [self.transformDatetype(index) for index in dfGraph.get(list(dfGraph.keys())[0])]
            x_data = [self.transformDatetype(x) for x in dfGraph[label_x[0]]]
        except TypeError:
            x = [index for index in dfGraph.get(list(dfGraph.keys())[0])]
            x_data = [x for x in dfGraph[label_x[0]]]
        
        bottom= [0 for _ in range(len(x))]
        
        for i in range(1, len(label_x)):
            # y axis data
            y_data = [float(y) for y in dfGraph[label_x[i-1 if i == len(label_x) else i]]]
            ax.bar(
                x_data if (x_data != [None]) and (x_data != None) else label_x[0],
                y_data,
                lw= bar['width'],
                color= bar['colors'][i % len(bar['colors'])],
                align= bar['align'],
                bottom= bottom
            )
            if bar['stack']:
                bottom = [ before + after for before, after in zip(bottom, y_data)]

                # View Max Value Text
                if general['value_text']:
                    max_y = np.max(bottom)
                    max_x = bottom.index(max_y)
                    ax.text(max_x-0.25, max_y, f'{max_y}', ha='left', va='top')
            else:
                bottom = 0
                
                # View Max Value Text
                if general['value_text']:
                    max_y = np.max(y_data)
                    max_x = y_data.index(max_y)
                    ax.text(max_x-0.25, max_y, f'{max_y}', ha='left', va='top')
            
            
        plt.title(general['title'], loc='center')
        plt.xlim((x_axis['min'], x_axis['max']))
        plt.ylim((y_axis['min'], y_axis['max']))
        plt.xlabel(x_axis['label'], fontsize=x_axis['labelsize'])
        plt.ylabel(y_axis['label'], fontsize=y_axis['labelsize'])
        plt.xticks(rotation = x_axis['ticks'], fontsize=x_axis['fontsize'])
        # 표현해야 될 데이터 많을 시 x 축 값 정리
        if len(x) > 10:
            ax.set_xticks(range(0, len(x), round(10 % len(x))))
            
        plt.yticks(rotation = y_axis['ticks'], fontsize=y_axis['fontsize'])
        plt.grid(visible=overlay['grid'])
        
        # legend on/off
        if overlay['legend']:
            plt.legend(title= legend['title'], labels = label_x[1:] if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=general['dpi'], bbox_inches='tight')
        plt.close()
        
        # Base64 encoding
        import base64
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return f'data:image/png;base64,{__convBase64}" width="{general["img_width"]}px"'
    
    
    # # 05.20 그래프 분리
    # # Twin Graph
    def twin(self, option = dict):
        """## Twin Graph

        ### Args:
            general (dict): 
                ```
                'general': {
                    'graph_style': 'ggplot', # graph view style
                    'fig_size': (12, 5), # graph size  tuple
                    'title': None, # graph title  str
                    'label': _data.columns if _data != None else None, # legend label  list | series
                    'flip': False, # Flip X-Y axis  True, False
                    'drop_columns': False, # Drop Column on Graph  True, False
                    'drop_columns_name': [''], # Drop Column Name  list[str]
                    'drop_column_axis': 0, # Drop Column Axis  0 - horizental, 1 - vertical
                    'dpi': 150, # Graph Resolution  default 150
                    'img_width': 700, # Image px  default 700
                    'value_text': False, # View Max Value Text  default False
                }
                ```
            x_axis (dict): 
                ```
                'x_axis': {
                    'label': None, # x axis label  str
                    'labelsize': 12, # x label fontsize  default 12
                    'fontsize': 7, # x label fontsize  default 7
                    'ticks': 45, # x label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            y_axis (dict):
                ```
                'y_axis': {
                    'label': None, # y axis label  str
                    'labelsize': 12, # y label fontsize  default 12
                    'fontsize': 5, # y label fontsize  default 5
                    'ticks': 0, # y label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            overlay (dict): 
                ```
                'overlay': {
                    'grid': True, # graph in grid background  True, False
                    'legend': True, # graph on legend On / Off  True, False
                }
                ```
            legend (dict): 
                ```
                'legend': {
                    'title': None, # legend title  str
                    'labels': None, # legend label  columns
                    'location': ''upper left', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
                    'fontsize': 7, # legend fontsize  int
                }
                ```
            line (dict):
                ```
                'line': {
                    'width': 1, # Line Width  float over 0
                    'style': '-', # Line Style  default = '-', '--' '-.' ':'
                    'colors': __SPLUNK_BASE_COLOR_MAP['base'], # Bar Colors  default on SPLUNK color map
                    'marker': 'o', # draw line on marker           
                    'marker_size': 5, # marker size
                }
                ```
            bar (dict):
                ```
                'bar': {
                    'width': 0.8, # Bar Width  float over 0
                    'colors': __SPLUNK_BASE_COLOR_MAP['categorical_2'], # Bar Colors  default on SPLUNK color map
                    'stack': True, # Bar values Stacked  True, False
                    'align': 'center', # Bar align  default center, edge
                }
                ```
            twin (dict):
                ```
                'twin': {
                    'twin': 'x', # Twin Axis  default x  y
                    'x_label': '', # Twin x label  str
                    'y_label': '', # Twin y label  str
                    'x_min': 0, # Twin x min value  float
                    'x_max': None, # Twin x max value  float
                    'y_min': 0, # Twin y min value  float
                    'y_max': None, # Twin y max value  float
                    'legend': 'upper right', # Second Legend location  default 'upper right'
                    'legend_fontsize': 7, # legend fontsize  int
                    'tight_layout': False, # graph layout margin  True, False
                }
        """
        updatedOption = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
        general = updatedOption['general']
        x_axis = updatedOption['x_axis']
        y_axis = updatedOption['y_axis']
        legend = updatedOption['legend']
        overlay = updatedOption['overlay']
        line = updatedOption['line']
        bar = updatedOption['bar']
        twin = updatedOption['twin']
        
        plt.style.use(general['graph_style'])
        
        # 원본 보존을 위한 copy
        data = self._data.copy()
        
        # column 삭제 유무
        if general['drop_columns']:
            for col in general['drop_columns_name']:
                for item in data:
                    if col in item:
                        del item[col]
        
        # base64 Encoding을 위한 bytesIO
        __graphToBytes = BytesIO()

        # Draw Graph
        dfGraph = {key: [d[key] for d in data if key in d] for key in data[0].keys()}
        _, axBar = plt.subplots(figsize=general['fig_size'])
        
        # prevent scientific notation
        plt.ticklabel_format(style='plain', axis='y')

        # Graph legend label
        label_x = list(dfGraph.keys())
        
        # x datas
        try:
            x = [self.transformDatetype(index) for index in dfGraph.get(list(dfGraph.keys())[0])]
            x_data = [self.transformDatetype(x) for x in dfGraph[label_x[0]]]
        except TypeError:
            x = [index for index in dfGraph.get(list(dfGraph.keys())[0])]
            x_data = [x for x in dfGraph[label_x[0]]]
            
        bottom= [0 for _ in range(len(x))]
        
        # Bar Graph
        for i in range(1, len(label_x)):
            # y axis data
            y_data = [float(y) for y in dfGraph[label_x[i-1 if i == len(label_x) else i]]]
            axBar.bar(
                x_data if (x_data != [None]) and (x_data != None) else label_x[0],
                y_data,
                lw= bar['width'],
                color= bar['colors'][i % len(bar['colors'])],
                align= bar['align'],
                bottom= bottom
            )
            if bar['stack']:
                bottom = [ before + after for before, after in zip(bottom, y_data)]
                
                # View Max Value Text
                if general['value_text']:
                    max_y = np.max(bottom)
                    max_x = bottom.index(max_y)
                    axBar.text(max_x-0.25, max_y, f'{max_y}', ha='left', va='top')
            else:
                bottom = 0
                
                # View Max Value Text
                if general['value_text']:
                    max_y = np.max(y_data)
                    max_x = y_data.index(max_y)
                    axBar.text(max_x-0.25, max_y, f'{max_y}', ha='left', va='top')
        
        plt.title(general['title'], loc='center')
        plt.xlim((x_axis['min'], x_axis['max']))
        plt.ylim((y_axis['min'], y_axis['max']))
        plt.xlabel(x_axis['label'], fontsize=x_axis['labelsize'])
        plt.ylabel(y_axis['label'], fontsize=y_axis['labelsize'])
        plt.xticks(rotation = x_axis['ticks'], fontsize=x_axis['fontsize'])
        # 표현해야 될 데이터 많을 시 x 축 값 정리
        if len(x) > 10:
            axBar.set_xticks(range(0, len(x), round(10 % len(x))))
            
        plt.yticks(rotation = y_axis['ticks'], fontsize=y_axis['fontsize'])
        
        # legend on/off
        if overlay['legend']:
            plt.legend(title= 'Bar', labels = label_x[1:] if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
        # Twinx | Twiny
        axLine = axBar.twinx() if twin['twin'] == 'x' else axBar.twiny()
        
        # prevent scientific notation
        plt.ticklabel_format(style='plain', axis='y')
        
        # Line Graph
        for i in range(1, len(label_x)):
            # y axis data
            y_data = [float(y) for y in dfGraph[label_x[i-1 if i == len(label_x) else i]]]
            axLine.plot(
                x_data,
                y_data,
                marker= line['marker'],
                markersize= line['marker_size'],
                lw= line['width'],
                color=line['colors'][i % len(line['colors'])],
            )
            
            # View Max Value Text
            if general['value_text']:
                max_y = np.max(y_data)
                max_x = y_data.index(max_y)
                axLine.text(max_x, max_y, f'{max_y}', ha='left', va='top')
        
        plt.xlim((twin['x_min'], twin['x_max']))
        plt.ylim((twin['y_min'], twin['y_max']))
        plt.ylabel(twin['y_label'], fontsize=y_axis['labelsize'])
        plt.yticks(rotation = y_axis['ticks'], fontsize=y_axis['fontsize'])
        plt.grid(visible=overlay['grid'])
        
        # legend on/off
        if overlay['legend']:
            plt.legend(title= 'Line', labels = label_x[1:] if legend['labels'] is None else legend['labels'], loc=twin['legend'], fontsize=twin['legend_fontsize'])
        
        # tight_layout
        if twin['tight_layout']:
            plt.tight_layout()        
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=general['dpi'], bbox_inches='tight')
        plt.close()
        
        # Base64 encoding
        import base64
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return f'data:image/png;base64,{__convBase64}" width="{general["img_width"]}px"'
    
    
    # 05.20 그래프 분리
    # Pie Graph
    def pie(self, option = dict):
        """## Pie Graph

        ### Args:
            general (dict): 
                ```
                'general': {
                    'graph_style': 'ggplot', # graph view style
                    'fig_size': (12, 5), # graph size  tuple
                    'title': None, # graph title  str
                    'label': _data.columns if _data != None else None, # legend label  list | series
                    'flip': False, # Flip X-Y axis  True, False
                    'drop_columns': False, # Drop Column on Graph  True, False
                    'drop_columns_name': [''], # Drop Column Name  list[str]
                    'drop_column_axis': 0, # Drop Column Axis  0 - horizental, 1 - vertical
                    'dpi': 150, # Graph Resolution  default 150
                    'img_width': 700, # Image px  default 700
                    'value_text': False, # View Max Value Text  default False
                }
                ```
            overlay (dict): 
                ```
                'overlay': {
                    'grid': True, # graph in grid background  True, False
                    'legend': True, # graph on legend On / Off  True, False
                }
                ```
            legend (dict): 
                ```
                'legend': {
                    'title': None, # legend title  str
                    'labels': None, # legend label  columns
                    'location': ''upper left', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
                    'fontsize': 7, # legend fontsize  int
                }
                ```
            pie (dict):
                ```
                'pie': {
                    'autopct': '%.2f%%', # display percentage  default %.2f%%
                    'labeldistance': 1.1, # label <-> pie distance  default 1.1  float
                    'startangle': 0, # Start point angle  default 0
                    'shadow': False, # Shadow On / Off  True, False
                    'radius': 1, # Pie Radius  float
                    'colors': __SPLUNK_BASE_COLOR_MAP['categorical_3'], # Pie Colors  default on SPLUNK color map
                    'wedge_width': None, # Pie To Donut width  float
                    'wedge_edge_color': None, # Pie To Donut color  default following matplotlib colors 
                    'explode': None # Pie piece Explode  tuple[float]     **tuple len == explode len**
                    'arrow': True, # Arrow option on / off  True, False
                }
                ```
        """
        updatedOption = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
        general = updatedOption['general']
        legend = updatedOption['legend']
        overlay = updatedOption['overlay']
        pie = updatedOption['pie']
        
        plt.style.use(general['graph_style'])
        
        # 원본 보존을 위한 copy
        data = self._data.copy()
        
        # column 삭제 유무
        if general['drop_columns']:
            for col in general['drop_columns_name']:
                for item in data:
                    if col in item:
                        del item[col]
        
        # base64 Encoding을 위한 bytesIO
        __graphToBytes = BytesIO()

        # Draw Graph
        dfGraph = {key: [d[key] for d in data if key in d] for key in data[0].keys()}
        _, ax = plt.subplots(figsize=general['fig_size'])
        
        # Graph legend label
        label_x = list(dfGraph.keys())
        
        # Total Column for Pie Chart 100%
        totalYdata = [sum(float(value) for value in values) for key, values in dfGraph.items() if key != label_x[0]]
        
        # label 개수가 2개 이하인 경우 단일 column의 값 기준으로 그래프 표시
        checkLabelLength = len(label_x)
        if checkLabelLength <= 2:
            totalYdata = dfGraph.get(label_x[1])
            label_x = [v for v in dfGraph[label_x[0]]]
        
        # Arrow Between PieGraph and the Label
        if pie['arrow']:
            _, ax = plt.subplots(figsize=general['fig_size'], subplot_kw=dict(aspect="equal"))
            
            wedges, _, _ = ax.pie(
                totalYdata,
                autopct=pie['autopct'],
                startangle=pie['startangle'],
                explode=pie['explode'],
                shadow=pie['shadow'],
                colors=pie['colors'],
                wedgeprops=dict(width=pie['wedge_width'], edgecolor=pie['wedge_edge_color']),
                radius=pie['radius']
            )
            
            # Pie piece와 Label 간 선 연결
            for i, p in enumerate(wedges):
                ang = (p.theta2 - p.theta1)/2. + p.theta1
                
                y_pos = np.sin(np.deg2rad(ang))
                x_pos = np.cos(np.deg2rad(ang))
                horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x_pos))]
                
                # 180도 일 경우 직선으로 표기하기 위한 조건
                connectionstyle = f"angle,angleA=0,angleB={ang}" if ang != 180.0 else "angle3,angleA=0,angleB=180"
                
                kw = dict(arrowprops=dict(arrowstyle="-", color=pie['colors'][i % len(pie['colors'])], linewidth=1.5), zorder=0, va="center")
                kw["arrowprops"].update({"connectionstyle": connectionstyle})
                
                ax.annotate(label_x[i+1] if checkLabelLength > 2 else label_x[i], xy=(x_pos, y_pos), xytext=(1.35*np.sign(x_pos), 1.4*y_pos),
                            horizontalalignment=horizontalalignment, **kw)

        else:
            ax.pie(
                totalYdata,
                autopct= pie['autopct'],
                startangle= pie['startangle'],
                explode= pie['explode'],
                shadow= pie['shadow'],
                radius= pie['radius'],
                colors= pie['colors'],
                wedgeprops=dict(width=pie['wedge_width'], edgecolor=pie['wedge_edge_color'])
            )        
        
        plt.title(general['title'], loc='center')
        
        # legend on/off
        if overlay['legend']:
            plt.legend(title= legend['title'], labels = label_x[1:] if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=general['dpi'], bbox_inches='tight')
        plt.close()
        
        # Base64 encoding
        import base64
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return f'data:image/png;base64,{__convBase64} width={general["img_width"]}px'