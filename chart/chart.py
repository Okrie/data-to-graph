# coding=utf-8
"""
    Data To Graph
    Author: Okrie
"""

import matplotlib.pyplot as plt
# import pandas as pd
import json
import dateutil.parser
import numpy as np
from io import BytesIO, StringIO


# 현재 불러 오지 못하는 문제가 있어 보류
# 한글 폰트 문제 해결 
# matplotlib은 한글 폰트를 지원하지 않음
# os정보
# import platform

# # font_manager : 폰트 관리 모듈
# # rc : 폰트 변경 모듈
# from matplotlib import font_manager, rc
# font_manager.fontManager
# # unicode 설정
# plt.rcParams['axes.unicode_minus'] = False

# if platform.system() == 'Darwin': # macos
#     rc('font', family='AppleGothic')
# elif platform.system() == 'Windows': # windows
#     path = 'c:/Windows/Fonts/malgun.ttf'
#     font_name = font_manager.FontProperties(fname=path).get_name()
#     rc('font', family=font_name)
# else:
#     print("Unknown System")
#     plt.rc('font', family='Nanum Gothic')
### Graph 한글 깨짐 현상 해결 끝 ###


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
            'fig_size': (5, 2),    # graph size        tuple
            
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
            'dpi': 150,             # Graph Resolution              default = 100
            'img_width': 700        # Image px                      default = 700
        },
        'x_axis': {
            'label': None,          # x axis label                  str
            'labelsize': 12,        # x label fontsize              default 5
            'fontsize': 7,         # x label fontsize              default 5
            'ticks': 45,            # x label text rotate degree    -90 ~ 90
            'min' : None,           # limit low value
            'max' : None,           # limit high value
        },
        'y_axis': {
            'label': None,          # y axis label                  str
            'labelsize': 12,        # x label fontsize              default 5
            'fontsize': 5,         # y label fontsize              default 5
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
            'location': 'best',     # legend location               best, left, center, right, upper [left, center, right], lower [left, center, right]
            'fontsize': 5,          # legend fontsize               int
        },
        'line': {
            'width': 1,             # Line Width                    float over 0
            'style': '-',           # Line Style                    default = '-', '--' '-.' ':'
            'colors': __SPLUNK_BASE_COLOR_MAP['base'], # Line Colors    default on SPLUNK color map
            # Marker
            'marker': None,          # draw line on marker
            'marker_size': 5,       # marker size
        },
        'bar': {
            'width': 1,             # Bar Width                     float over 0
            'colors': __SPLUNK_BASE_COLOR_MAP['categorical_2'], # Bar Colors    default on SPLUNK color map
            'stack': True,          # Bar values Stacked            True, False
            'align': None,          # Bar align                     center, edge
        },
        'twin': {
            'twin': 'x',            # Twin Axis                     default x  y
            'x_label': '',          # Twin x label                  str
            'y_label': '',          # Twin y label                  str
            'x_min': None,          # Twin x min value              float
            'x_max': None,          # Twin x max value              float
            'y_min': None,          # Twin y min value              float
            'y_max': None,          # Twin y max value              float
            'legend': 'upper right',# Second Legend location        default 'upper right'
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
            'arrow': False,         # Arrow option on / off         True, False
        },
    }
    
    def __init__(self):
        # print(self._data)
        self._data = []
        pass
    
    # pandas 제거로 사용 하지 않음
    # 받은 데이터가 한개, 한개 이상일 때로 구분하여 DataFrame 형태로 변경
    # def seperateJSONResult(self, originJsonData = None, index: str = None):
    #     __jsonType = type(originJsonData)
        
    #     # Result 데이터가 1개 일때
    #     if __jsonType == dict:
    #         __jsondata = pd.read_json(StringIO(originJsonData))
    #         __jsondata = __jsondata.to_frame().T
            
    #     # Result 데이터가 1개 이상 일 때
    #     else:
    #         __jsondata = pd.DataFrame.from_records(originJsonData)

    #     __jsondata.reset_index(drop=True, inplace=True)
        
    #     # index로 지정할 컬럼 유무 체크
    #     try:
    #         if '_time' in __jsondata.columns:
    #             __jsondata['_time'] = __jsondata['_time'].astype(dtype='str', errors='ignore')
    #             __jsondata['_time'] = __jsondata['_time'].apply(self.transformDatetype)
    #         __jsondata.set_index(index if index != None else __jsondata.columns[0], inplace=True)
    #     except:
    #         print(__jsondata)
    #         raise print("Not Exist column for using index \n Check Columns")
            
        
    #     self._len = len(__jsondata)
        
    #     return __jsondata
    
    def seperateJSONResult_json(self, originJsonData = None, index: str = None):
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


    # pandas 제거로 사용 하지 않음
    # Graph를 그리기 위한 Data 정제 과정
    # 데이터를 받아 하나의 DataFrame으로 병합
    # def loadJsonDataToDataframe(self, jsondata: dict = None, index: str = None):
    #     """
    #         ## JsonData를 받아 Graph를 그리기 위해 DataFrame으로 정제

    #         ### Args:
    #             jsondata dict: JsonData

    #         ### Returns:
    #             self._data: Json Data To DataFrame
    #     """
    #     print(jsondata)
    #     __jsondata = self.seperateJSONResult(jsondata, index)
        
    #     # print(f' __len = {__len}')
    #     # if __len > 1:
    #     #     print("Data iS LIST TYPE")
    #     # else:
    #     #     print("Data iS DICT TYPE")
        
    #     # type object to str
    #     __jsondata = __jsondata.astype(dtype='str', errors='ignore')
        
    #     # type object to integer
    #     __jsondata = __jsondata.astype(dtype='int64', errors='ignore')
        
    #     # type object to datetime
    #     # __jsondata._time = __jsondata._time.apply(self.transform_datetype)
        
    #     self._data = pd.concat([self._data, __jsondata])

    #     return self._data
    
    
    def loadJsonDataToDict(self, jsondata: dict = None, index: str = None):
        json_data = self.seperateJSONResult_json(jsondata, index)
        
        self._data.extend(json_data)

        return self._data
    
    # 현재 미사용
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
                    'dpi': 200, # Graph Resolution  default = 200
                }
                ```
            x_axis (dict): 
                ```
                'x_axis': {
                    'label': None, # x axis label  str
                    'fontsize': 12, # x label fontsize  default 12
                    'ticks': 45, # x label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            y_axis (dict):
                ```
                'y_axis': {
                    'label': None, # y axis label  str
                    'fontsize': 12, # x label fontsize  default 12
                    'ticks': 0, # y label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            overlay (dict): 
                ```
                'overlay': {
                    'grid': True, # graph in grid background  True, False
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

        # print(f'Option \n {updatedOption}')
        general = updatedOption['general']
        x_axis = updatedOption['x_axis']
        y_axis = updatedOption['y_axis']
        legend = updatedOption['legend']
        overlay = updatedOption['overlay']
        line = updatedOption['line']
        
        plt.style.use(general['graph_style'])
        
        # 원본 보존을 위한 copy
        data = self._data.copy()
        
        # print('\n', data)
        
        # column 삭제 유무
        if general['drop_columns']:
            for col in general['drop_columns_name']:
                for item in data:
                    if col in item:
                        del item[col]

        # if general['drop_columns']:
        #     data.drop(general['drop_columns_name'], axis=general['drop_column_axis'], inplace=True)
        #     print(f"Deleted Column : {general['drop_columns']}\n{data}")
        
        # base64 Encoding을 위한 bytesIO
        __graphToBytes = BytesIO()

        # Draw Graph
        dfGraph = {key: [d[key] for d in data if key in d] for key in data[0].keys()}
        # dfGraph = data.copy() if not general['flip'] else data.T.copy()
        fig, ax = plt.subplots(figsize=general['fig_size'])
        
        # for item in data:
        #     print(item, '\n')
            
            
        x = []
        y = []
        label_x = []
        label_y = []
        
        tmp = {}
        
        for item in data:
            item = dict(item)
            label_x = list(item.keys())
            for _ in range(len(item)):
                x.append(self.transformDatetype(item[label_x[0]]))
                y.append(int(item[label_x[1]]))
        
        print(f"x = {x}")
        print(f"y = {y}")
        print(f"Label = {label_x}")
        # print(list(test.values())[1])
        ax.plot(
            x,
            y,
            marker= line['marker'],
            markersize= line['marker_size'],
            lw= line['width'],
            # color=line['colors']
        )
        
        # ax = plt.plot(
        #     times,
        #     log_levels,
        #     # kind='line',
        #     marker= line['marker'],
        #     markersize= line['marker_size'],
        #     lw= line['width'],
        #     label=list(dfGraph.values())[0],
        #     # color=line['colors']
        # )
        
        plt.title(general['title'], loc='center')
        plt.xlim((x_axis['min'], x_axis['max']))
        plt.ylim((y_axis['min'], y_axis['max']))
        plt.xlabel(x_axis['label'], fontsize=x_axis['labelsize'])
        plt.ylabel(y_axis['label'], fontsize=y_axis['labelsize'])
        plt.xticks(rotation = x_axis['ticks'], fontsize=x_axis['fontsize'])
        # print(len(label_x))
        # # 표현해야 될 데이터 많을 시 x 축 값 정리
        # if len(x) > 10:
        #     ax.set_xticks(np.arange(0, len(x)+1, round(len(label_x) % 10)))
            
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
        return "data:image/png;base64,%s" % __convBase64 + f" width={general['img_width']}px"
    
    
    # 05.20 그래프 분리
    # Bar Graph
    # def bar(self, option = dict):
    #     """## Bar Graph

    #     ### Args:
    #         general (dict): 
    #             ```
    #             'general': {
    #                 'graph_style': 'ggplot', # graph view style
    #                 'fig_size': (12, 5), # graph size  tuple
    #                 'title': None, # graph title  str
    #                 'label': _data.columns if _data != None else None, # legend label  list | series
    #                 'flip': False, # Flip X-Y axis  True, False
    #                 'drop_columns': False, # Drop Column on Graph  True, False
    #                 'drop_columns_name': [''], # Drop Column Name  list[str]
    #                 'drop_column_axis': 0, # Drop Column Axis  0 - horizental, 1 - vertical
    #                 'dpi': 200, # Graph Resolution  default = 200
    #             }
    #             ```
    #         x_axis (dict): 
    #             ```
    #             'x_axis': {
    #                 'label': None, # x axis label  str
    #                 'fontsize': 12, # x label fontsize  12
    #                 'ticks': 45, # x label text rotate degree  -90 ~ 90
    #                 'min' : None, # limit low value
    #                 'max' : None, # limit high value
    #             }
    #             ```
    #         y_axis (dict):
    #             ```
    #             'y_axis': {
    #                 'label': None, # y axis label  str
    #                 'fontsize': 12, # x label fontsize  12
    #                 'ticks': 0, # y label text rotate degree  -90 ~ 90
    #                 'min' : None, # limit low value
    #                 'max' : None, # limit high value
    #             }
    #             ```
    #         overlay (dict): 
    #             ```
    #             'overlay': {
    #                 'grid': True, # graph in grid background  True, False
    #                 'legend': True, # graph on legend On / Off  True, False
    #             }
    #             ```
    #         legend (dict): 
    #             ```
    #             'legend': {
    #                 'title': None, # legend title  str
    #                 'labels': None, # legend label  columns
    #                 'location': 'best', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
    #                 'fontsize': 7, # legend fontsize  int
    #             }
    #             ```
    #         bar (dict):
    #             ```
    #             'bar': {
    #                 'width': 1, # Bar Width  float over 0
    #                 'colors': __SPLUNK_BASE_COLOR_MAP['categorical_2'], # Bar Colors  default on SPLUNK color map
    #                 'stack': True, # Bar values Stacked  True, False
    #                 'align': None, # Bar align  center, edge
    #             }
    #             ```
    #     """
    #     updatedOption = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
    #     print(f'Option \n {updatedOption}')
    #     general = updatedOption['general']
    #     x_axis = updatedOption['x_axis']
    #     y_axis = updatedOption['y_axis']
    #     legend = updatedOption['legend']
    #     overlay = updatedOption['overlay']
    #     bar = updatedOption['bar']
        
    #     plt.style.use(general['graph_style'])
        
    #     # 원본 보존을 위한 copy
    #     data = self._data.copy()
        
    #     # column 삭제 유무
    #     if general['drop_columns']:
    #         data.drop(general['drop_columns_name'], axis=general['drop_column_axis'], inplace=True)
    #         print(f"Deleted Column : {general['drop_columns']}\n{data}")
        
    #     # base64 Encoding을 위한 bytesIO
    #     __graphToBytes = BytesIO()

    #     # Draw Graph
    #     dfGraph = data.copy() if not general['flip'] else data.T.copy()
    #     plt.figure(figsize=general['fig_size'])
        
    #     # print(dfGraph)
            
    #     ax = dfGraph.plot(
    #         kind = 'bar',
    #         stacked= bar['stack'],
    #         lw= bar['width'],
    #         color= bar['colors']
    #     )
        
    #     plt.title(general['title'], loc='center')
    #     plt.xlim((x_axis['min'], x_axis['max']))
    #     plt.ylim((y_axis['min'], y_axis['max']))
    #     plt.xlabel(x_axis['label'], fontsize=x_axis['fontsize'])
    #     plt.ylabel(y_axis['label'])
    #     plt.xticks(rotation = x_axis['ticks'])
    #     # 표현해야 될 데이터 많을 시 x 축 값 정리
    #     if len(dfGraph.index) > 10:
    #         ax.set_xticks(np.arange(0, len(dfGraph.index)+1, round(len(dfGraph.index) % 10)))
            
    #     plt.yticks(rotation = y_axis['ticks'])
    #     plt.grid(visible=overlay['grid'])
        
    #     # legend on/off
    #     if overlay['legend']:
    #         plt.legend(title= legend['title'], labels = data.columns if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
    #     # Graph PNG Setting
    #     plt.savefig(__graphToBytes, format='png', dpi=200, bbox_inches='tight')
    #     plt.close()
        
    #     # Base64 encoding
    #     import base64
    #     __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
    #     return "data:image/png;base64,%s" % __convBase64
    
    
    # # 05.20 그래프 분리
    # # Twin Graph
    # def twin(self, option = dict):
    #     """## Twin Graph

    #     ### Args:
    #         general (dict): 
    #             ```
    #             'general': {
    #                 'graph_style': 'ggplot', # graph view style
    #                 'fig_size': (12, 5), # graph size  tuple
    #                 'title': None, # graph title  str
    #                 'label': _data.columns if _data != None else None, # legend label  list | series
    #                 'flip': False, # Flip X-Y axis  True, False
    #                 'drop_columns': False, # Drop Column on Graph  True, False
    #                 'drop_columns_name': [''], # Drop Column Name  list[str]
    #                 'drop_column_axis': 0, # Drop Column Axis  0 - horizental, 1 - vertical
    #                 'dpi': 200, # Graph Resolution  default = 200
    #             }
    #             ```
    #         x_axis (dict): 
    #             ```
    #             'x_axis': {
    #                 'label': None, # x axis label  str
    #                 'fontsize': 12, # x label fontsize  12
    #                 'ticks': 45, # x label text rotate degree  -90 ~ 90
    #                 'min' : None, # limit low value
    #                 'max' : None, # limit high value
    #             }
    #             ```
    #         y_axis (dict):
    #             ```
    #             'y_axis': {
    #                 'label': None, # y axis label  str
    #                 'fontsize': 12, # x label fontsize  12
    #                 'ticks': 0, # y label text rotate degree  -90 ~ 90
    #                 'min' : None, # limit low value
    #                 'max' : None, # limit high value
    #             }
    #             ```
    #         overlay (dict): 
    #             ```
    #             'overlay': {
    #                 'grid': True, # graph in grid background  True, False
    #                 'legend': True, # graph on legend On / Off  True, False
    #             }
    #             ```
    #         legend (dict): 
    #             ```
    #             'legend': {
    #                 'title': None, # legend title  str
    #                 'labels': None, # legend label  columns
    #                 'location': 'best', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
    #                 'fontsize': 7, # legend fontsize  int
    #             }
    #             ```
    #         line (dict):
    #             ```
    #             'line': {
    #                 'width': 1, # Line Width  float over 0
    #                 'style': '-', # Line Style  default = '-', '--' '-.' ':'
    #                 'colors': None, # Line Colors  default following matplotlib colors    
    #                 'marker': 'o', # draw line on marker           
    #                 'marker_size': 5, # marker size
    #             }
    #             ```
    #         bar (dict):
    #             ```
    #             'bar': {
    #                 'width': 1, # Bar Width  float over 0
    #                 'colors': None, # Bar Colors  default following matplotlib colors    
    #                 'stack': True, # Bar values Stacked  True, False
    #                 'align': None, # Bar align  left, center, right
    #             }
    #             ```
    #         twin (dict):
    #             ```
    #             'twin': {
    #                 'twin': 'x', # Twin Axis  default x  y
    #                 'x_label': '', # Twin x label  str
    #                 'y_label': '', # Twin y label  str
    #                 'x_min': None, # Twin x min value  float
    #                 'x_max': None, # Twin x max value  float
    #                 'y_min': None, # Twin y min value  float
    #                 'y_max': None, # Twin y max value  float
    #                 'legend': 'upper right', # Second Legend location  default 'upper right'
    #                 'legend_fontsize': 7, # legend fontsize  int
    #                 'tight_layout': False, # graph layout margin  True, False
    #             }
    #     """
    #     updatedOption = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
    #     print(f'Option \n {updatedOption}')
    #     general = updatedOption['general']
    #     x_axis = updatedOption['x_axis']
    #     y_axis = updatedOption['y_axis']
    #     legend = updatedOption['legend']
    #     overlay = updatedOption['overlay']
    #     line = updatedOption['line']
    #     bar = updatedOption['bar']
    #     twin = updatedOption['twin']
        
    #     plt.style.use(general['graph_style'])
        
    #     # 원본 보존을 위한 copy
    #     data = self._data.copy()
        
    #     # column 삭제 유무
    #     if general['drop_columns']:
    #         data.drop(general['drop_columns_name'], axis=general['drop_column_axis'], inplace=True)
    #         print(f"Deleted Column : {general['drop_columns']}\n{data}")
        
    #     # base64 Encoding을 위한 bytesIO
    #     __graphToBytes = BytesIO()

    #     # Draw Graph
    #     dfGraph = data.copy() if not general['flip'] else data.T.copy()
    #     fig, bargraph = plt.subplots(figsize=general['fig_size'])
        
    #     # print(dfGraph)
        
    #     # Bar Graph
    #     ax = dfGraph.plot(
    #         kind = 'bar',
    #         stacked= bar['stack'],
    #         lw= bar['width'],
    #         color= bar['colors'],
    #         align= bar['align'],
    #         ax=bargraph,
    #     )
        
    #     plt.title(general['title'], loc='center')
    #     plt.xlim((x_axis['min'], x_axis['max']))
    #     plt.ylim((y_axis['min'], y_axis['max']))
    #     plt.xlabel(x_axis['label'])
    #     plt.ylabel(y_axis['label'])
    #     plt.xticks(rotation = x_axis['ticks'])        
    #     # 표현해야 될 데이터 많을 시 x 축 값 정리
    #     if len(dfGraph.index) > 10:
    #         ax.set_xticks(np.arange(0, len(dfGraph.index)+1, round(len(dfGraph.index) % 10)))
        
    #     plt.yticks(rotation = y_axis['ticks'])
        
    #     # legend on/off
    #     if overlay['legend']:
    #         plt.legend(title='Bar', labels = data.columns if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
    #     # Twinx | Twiny
    #     linegraph = bargraph.twinx() if twin['twin'] == 'x' else bargraph.twiny()
        
    #     # Line Graph
    #     dfGraph.plot(
    #         marker= line['marker'],
    #         markersize= line['marker_size'],
    #         lw= line['width'],
    #         color=line['colors'],
    #         ax=linegraph,
    #     )
        
    #     plt.xlim((twin['x_min'], twin['x_max']))
    #     plt.ylim((twin['y_min'], twin['y_max']))
    #     plt.xlabel(twin['x_label'])
    #     plt.ylabel(twin['y_label'])
    #     plt.grid(visible=overlay['grid'])
        
    #     # legend on / off
    #     if overlay['legend']:
    #         plt.legend(title='Line', labels = data.columns if legend['labels'] is None else legend['labels'], loc=twin['legend'], fontsize=twin['legend_fontsize'])
        
    #     # tight_layout
    #     if twin['tight_layout']:
    #         plt.tight_layout()        
        
    #     # Graph PNG Setting
    #     plt.savefig(__graphToBytes, format='png', dpi=200, bbox_inches='tight')
    #     plt.close()
        
    #     # Base64 encoding
    #     import base64
    #     __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
    #     return "data:image/png;base64,%s" % __convBase64
    
    
    # # 05.20 그래프 분리
    # # Pie Graph
    # def pie(self, option = dict):
    #     """## Pie Graph

    #     ### Args:
    #         general (dict): 
    #             ```
    #             'general': {
    #                 'graph_style': 'ggplot', # graph view style
    #                 'fig_size': (12, 5), # graph size  tuple
    #                 'title': None, # graph title  str
    #                 'label': _data.columns if _data != None else None, # legend label  list | series
    #                 'flip': False, # Flip X-Y axis  True, False
    #                 'drop_columns': False, # Drop Column on Graph  True, False
    #                 'drop_columns_name': [''], # Drop Column Name  list[str]
    #                 'drop_column_axis': 1, # Drop Column Axis  0 - horizental, 1 - vertical
    #                 'dpi': 200, # Graph Resolution  default = 200
    #             }
    #             ```
    #         overlay (dict): 
    #             ```
    #             'overlay': {
    #                 'grid': True, # graph in grid background  True, False
    #                 'legend': True, # graph on legend On / Off  True, False
    #             }
    #             ```
    #         legend (dict): 
    #             ```
    #             'legend': {
    #                 'title': None, # legend title  str
    #                 'labels': None, # legend label  columns
    #                 'location': 'best', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
    #                 'fontsize': 7, # legend fontsize  int
    #             }
    #             ```
    #         pie (dict):
    #             ```
    #             'pie': {
    #                 'autopct': '%.2f%%', # display percentage  default %.2f%%
    #                 'labeldistance': 1.1, # label <-> pie distance  default 1.1  float
    #                 'startangle': 0, # Start point angle  default 0
    #                 'shadow': False, # Shadow On / Off  True, False
    #                 'radius': 1, # Pie Radius  float
    #                 'colors': None, # Pie Colors  default following matplotlib colors    
    #                 'wedge_width': 0.5, # Pie To Donut width  default 0.5  float
    #                 'wedge_edge_color': None, # Pie To Donut color  default following matplotlib colors 
    #                 'explode': None # Pie piece Explode  tuple[float]     **tuple len == explode len**
    #                 'arrow': False, # Arrow option on / off  True, False
    #             }
    #             ```
    #     """
    #     updatedOption = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
    #     print(f'Option \n {updatedOption}')
    #     general = updatedOption['general']
    #     legend = updatedOption['legend']
    #     overlay = updatedOption['overlay']
    #     pie = updatedOption['pie']
        
    #     plt.style.use(general['graph_style'])
        
    #     # 원본 보존을 위한 copy
    #     data = self._data.copy()
        
    #     # column 삭제 유무
    #     if general['drop_columns']:
    #         data.drop(general['drop_columns_name'], axis=general['drop_column_axis'], inplace=True)
    #         print(f"Deleted Column : {general['drop_columns_name']}\n{data}")
        
    #     # base64 Encoding을 위한 bytesIO
    #     __graphToBytes = BytesIO()

    #     # Draw Graph
    #     dfGraph = data.copy() if not general['flip'] else data.T.copy()
    #     plt.figure(figsize=general['fig_size'])
        
    #     # print(dfGraph)
        
    #     # Total Column for Pie Chart 100%
    #     dfGraph.loc['Total', :] = dfGraph[dfGraph.columns].sum()
    #     dfGraph = dfGraph.T
        
    #     # Arrow Between PieGraph and the Label
    #     if pie['arrow']:
    #         _, ax = plt.subplots(figsize=general['fig_size'], subplot_kw=dict(aspect="equal"))
            
    #         wedges, _, _ = ax.pie(
    #             dfGraph['Total'].values,
    #             autopct=pie['autopct'],
    #             startangle=pie['startangle'],
    #             explode=pie['explode'],
    #             shadow=pie['shadow'],
    #             colors=pie['colors'],
    #             wedgeprops=dict(width=pie['wedge_width'], edgecolor=pie['wedge_edge_color']),
    #             radius=pie['radius']
    #         )
            
    #         # Pie piece와 Label 간 선 연결
    #         for i, p in enumerate(wedges):
    #             ang = (p.theta2 - p.theta1)/2. + p.theta1
    #             y = np.sin(np.deg2rad(ang))
    #             x = np.cos(np.deg2rad(ang))
    #             horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
                
    #             connectionstyle = f"angle,angleA=0,angleB={ang}"
    #             kw = dict(arrowprops=dict(arrowstyle="-", color=pie['colors'][i], linewidth=1.5), zorder=0, va="center")
    #             kw["arrowprops"].update({"connectionstyle": connectionstyle})
                
    #             ax.annotate(data.columns[i], xy=(x, y), xytext=(1.25*np.sign(x), 1.3*y),
    #                         horizontalalignment=horizontalalignment, **kw)

    #     else:
    #         dfGraph['Total'].plot.pie(
    #             autopct= pie['autopct'],
    #             startangle= pie['startangle'],
    #             explode= pie['explode'],
    #             shadow= pie['shadow'],
    #             radius= pie['radius'],
    #             colors= pie['colors'],
    #             wedgeprops=dict(width=pie['wedge_width'], edgecolor=pie['wedge_edge_color'])
    #         )        
        
    #     plt.title(general['title'], loc='center')
    #     if overlay['legend']:
    #         plt.legend(title= legend['title'], labels = data.columns if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
    #     # Graph PNG Setting
    #     plt.savefig(__graphToBytes, format='png', dpi=200, bbox_inches='tight')
    #     plt.close()
        
    #     # Base64 encoding
    #     import base64
    #     __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
    #     return "data:image/png;base64,%s" % __convBase64
