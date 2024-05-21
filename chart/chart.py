# coding=utf-8
"""
    Data To Graph
    Author: Okrie
"""

import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO, StringIO
import json
from datetime import datetime

class drawChart:
    """
        ## Data To Graph

        ### Returns:
            - Web에서 사용하기 위한 Graph PNG를 Base64로 인코딩해 Return
            
            line: 선그래프
            bar: 막대형 그래프
            twin: 선, 막대 혼합 그래프
            pie: 원 그래프
    """
    _data: pd.DataFrame = None
    _len: int = 0
    
    # OPTIONS
    DEFAULT_OPTION: dict = {
        'general': {
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
            
            # DropColumns
            'drop_columns': False,  # Drop Column on Graph          True, False
            'drop_columns_name': [''], # Drop Column Name           list[str]
            'drop_column_axis': 1,  # Drop Column Axis              0 - horizental, 1 - vertical
            
            # Graph resolution
            'dpi': 200,             # Graph Resolution              default = 200
        },
        'x_axis': {
            'label': None,          # x axis label                  str
            'ticks': 45,            # x label text rotate degree    -90 ~ 90
            'min' : None,           # limit low value
            'max' : None,           # limit high value
        },
        'y_axis': {
            'label': None,          # y axis label                  str
            'ticks': 0,             # y label text rotate degree    -90 ~ 90
            'min' : None,           # limit low value
            'max' : None,           # limit high value
        },
        'legend': {
            'labels': None,         # legend label                  columns
            'location': 'best',     # legend location               best, left, center, right, upper [left, center, right], lower [left, center, right]
            'fontsize': 7,          # legend fontsize               int
        },
        'overlay': {
            ### GRID, AXIS
            'grid': True,           # graph in grid background      True, False
            'axis': 0,              # value axis                    0 - horizental, 1 - vertical
            
            ## GRAPH layout margin
            'tight_layout': False,  # graph layout margin           True, False
        },
        'line': {
            'width': 1,             # Line Width                    float over 0
            'style': '-',           # Line Style                    default = '-', '--' '-.' ':'
            'colors': None,         # Line Colors                   default following matplotlib colors    
            # Marker
            'marker': 'o',          # draw line on marker           
            'marker_size': 5,       # marker size
        },
        'bar': {
            'width': 1,             # Bar Width                     float over 0
            'colors': None,         # Bar Colors                    default following matplotlib colors    
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
        },
        'pie': {
            'autopct': '%.2f%%',    # display percentage            default %.2f%%
            'labeldistance': 1.1,   # label <-> pie distance        default 1.1  float
            'startangle': 0,        # Start point angle             default 0
            'shadow': False,        # Shadow On / Off               True, False
            'radius': 1,            # Pie Radius                    float
            'colors': None,         # Pie Colors                    default following matplotlib colors    
            'wedge_width': None,    # Pie To Donut width            float
            'wedge_edge_color': None,# Pie To Donut color           default following matplotlib colors 
            'explode': None         # Pie piece Explode             tuple[float]     **tuple len == explode len**
        },
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
        """
            ## JsonData를 받아 Graph를 그리기 위해 DataFrame으로 정제

            ### Args:
                jsondata dict: JsonData

            ### Returns:
                self._data: Json Data To DataFrame
        """
        __jsondata = self.seperateJSONResult(jsondata)
        
        # print(f' __len = {__len}')
        # if __len > 1:
        #     print("Data iS LIST TYPE")
        # else:
        #     print("Data iS DICT TYPE")
        
        # type object to str
        __jsondata = __jsondata.astype(dtype='str', errors='ignore')
        
        # type object to integer
        __jsondata = __jsondata.astype(dtype='int64', errors='ignore')
        
        # type object to datetime
        # __jsondata._time = __jsondata._time.apply(self.tranform_datetype)
        
        self._data = pd.concat([self._data, __jsondata])

        return self._data
    
    
    # 현재 미사용
    # 시간 값을 년-월-일 시:분:초로 변경하는 과정
    @staticmethod
    def tranform_datetype(beforeDatetime):        
        return datetime.fromisoformat(beforeDatetime[:-5]).strftime('%Y-%m-%d %H:%M:%S')
    
    # 빈 옵션에 Default 옵션을 지정하기 위한 함수
    def optionUpdate(self, default_option, overrides_option):
        for k, v in overrides_option.items():
            if isinstance(v, dict) and k in default_option:
                default_option[k] = self.optionUpdate(default_option.get(k, {}), v)
            else:
                default_option[k] = v
        return default_option
    
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
                    'ticks': 45, # x label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            y_axis (dict):
                ```
                'y_axis': {
                    'label': None, # y axis label  str
                    'ticks': 0, # y label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            legend (dict): 
                ```
                'legend': {
                    'labels': None, # legend label  columns
                    'location': 'best', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
                    'fontsize': 7, # legend fontsize  int
                }
                ```
            overlay (dict): 
                ```
                'overlay': {
                    'grid': True, # graph in grid background  True, False
                    'axis': 0, # value axis  0 - horizental, 1 - vertical
                    'tight_layout': False, # graph layout margin  True, False
                }
                ```
            line (dict):
                ```
                'line': {
                    'width': 1, # Line Width  float over 0
                    'style': '-', # Line Style  default = '-', '--' '-.' ':'
                    'colors': None, # Line Colors  default following matplotlib colors    
                    'marker': 'o', # draw line on marker           
                    'marker_size': 5, # marker size
                }
                ```
        """
        updated_option = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
        print(f'Option \n {updated_option}')
        general = updated_option['general']
        x_axis = updated_option['x_axis']
        y_axis = updated_option['y_axis']
        legend = updated_option['legend']
        overlay = updated_option['overlay']
        line = updated_option['line']
        
        plt.style.use(general['graph_style'])
        
        # 원본 보존을 위한 copy
        data = self._data.copy()
        
        # column 삭제 유무
        if general['drop_columns']:
            data.drop(general['drop_columns_name'], axis=general['drop_column_axis'], inplace=True)
            print(f"Deleted Column : {general['drop_columns']}\n{data}")
        
        # base64 Encoding을 위한 bytesIO
        __graphToBytes = BytesIO()

        # Draw Graph
        dfGraph = data.copy() if not general['flip'] else data.T.copy()
        plt.figure(figsize=general['fig_size'])
        
        # print(dfGraph)
        
        dfGraph.plot(
            marker= line['marker'],
            markersize= line['marker_size'],
            lw= line['width'],
            color=line['colors']
        )
        
        plt.title(general['title'], loc='center')
        plt.xlim((x_axis['min'], x_axis['max']))
        plt.ylim((y_axis['min'], y_axis['max']))
        plt.xlabel(x_axis['label'])
        plt.ylabel(y_axis['label'])
        plt.xticks(rotation = x_axis['ticks'])
        plt.yticks(rotation = y_axis['ticks'])
        plt.grid(visible=overlay['grid'])
        plt.legend(labels = data.columns if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=200, bbox_inches='tight')
        plt.close()
        
        # Base64 encoding
        import base64
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,%s" % __convBase64
    
    
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
                    'dpi': 200, # Graph Resolution  default = 200
                }
                ```
            x_axis (dict): 
                ```
                'x_axis': {
                    'label': None, # x axis label  str
                    'ticks': 45, # x label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            y_axis (dict):
                ```
                'y_axis': {
                    'label': None, # y axis label  str
                    'ticks': 0, # y label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            legend (dict): 
                ```
                'legend': {
                    'labels': None, # legend label  columns
                    'location': 'best', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
                    'fontsize': 7, # legend fontsize  int
                }
                ```
            overlay (dict): 
                ```
                'overlay': {
                    'grid': True, # graph in grid background  True, False
                    'axis': 0, # value axis  0 - horizental, 1 - vertical
                    'tight_layout': False, # graph layout margin  True, False
                }
                ```
            bar (dict):
                ```
                'bar': {
                    'width': 1, # Bar Width  float over 0
                    'colors': None, # Bar Colors  default following matplotlib colors    
                    'stack': True, # Bar values Stacked  True, False
                    'align': None, # Bar align  center, edge
                }
                ```
        """
        updated_option = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
        print(f'Option \n {updated_option}')
        general = updated_option['general']
        x_axis = updated_option['x_axis']
        y_axis = updated_option['y_axis']
        legend = updated_option['legend']
        overlay = updated_option['overlay']
        bar = updated_option['bar']
        
        plt.style.use(general['graph_style'])
        
        # 원본 보존을 위한 copy
        data = self._data.copy()
        
        # column 삭제 유무
        if general['drop_columns']:
            data.drop(general['drop_columns_name'], axis=general['drop_column_axis'], inplace=True)
            print(f"Deleted Column : {general['drop_columns']}\n{data}")
        
        # base64 Encoding을 위한 bytesIO
        __graphToBytes = BytesIO()

        # Draw Graph
        dfGraph = data.copy() if not general['flip'] else data.T.copy()
        plt.figure(figsize=general['fig_size'])
        
        # print(dfGraph)
            
        dfGraph.plot(
            kind = 'bar',
            stacked= bar['stack'],
            lw= bar['width'],
            color= bar['colors']
        )
        
        plt.title(general['title'], loc='center')
        plt.xlim((x_axis['min'], x_axis['max']))
        plt.ylim((y_axis['min'], y_axis['max']))
        plt.xlabel(x_axis['label'])
        plt.ylabel(y_axis['label'])
        plt.xticks(rotation = x_axis['ticks'])
        plt.yticks(rotation = y_axis['ticks'])
        plt.grid(visible=overlay['grid'])
        plt.legend(labels = data.columns if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=200, bbox_inches='tight')
        plt.close()
        
        # Base64 encoding
        import base64
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,%s" % __convBase64
    
    
    # 05.20 그래프 분리
    # Twin Graph
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
                    'dpi': 200, # Graph Resolution  default = 200
                }
                ```
            x_axis (dict): 
                ```
                'x_axis': {
                    'label': None, # x axis label  str
                    'ticks': 45, # x label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            y_axis (dict):
                ```
                'y_axis': {
                    'label': None, # y axis label  str
                    'ticks': 0, # y label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            legend (dict): 
                ```
                'legend': {
                    'labels': None, # legend label  columns
                    'location': 'best', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
                    'fontsize': 7, # legend fontsize  int
                }
                ```
            overlay (dict): 
                ```
                'overlay': {
                    'grid': True, # graph in grid background  True, False
                    'axis': 0, # value axis  0 - horizental, 1 - vertical
                    'tight_layout': False, # graph layout margin  True, False
                }
                ```
            line (dict):
                ```
                'line': {
                    'width': 1, # Line Width  float over 0
                    'style': '-', # Line Style  default = '-', '--' '-.' ':'
                    'colors': None, # Line Colors  default following matplotlib colors    
                    'marker': 'o', # draw line on marker           
                    'marker_size': 5, # marker size
                }
                ```
            bar (dict):
                ```
                'bar': {
                    'width': 1, # Bar Width  float over 0
                    'colors': None, # Bar Colors  default following matplotlib colors    
                    'stack': True, # Bar values Stacked  True, False
                    'align': None, # Bar align  left, center, right
                }
                ```
            twin (dict):
                ```
                'twin': {
                    'twin': 'x', # Twin Axis  default x  y
                    'x_label': '', # Twin x label  str
                    'y_label': '', # Twin y label  str
                    'x_min': None, # Twin x min value  float
                    'x_max': None, # Twin x max value  float
                    'y_min': None, # Twin y min value  float
                    'y_max': None, # Twin y max value  float
                    'legend': 'upper right', # Second Legend location  default 'upper right'
                    'legend_fontsize': 7, # legend fontsize  int
                }
        """
        updated_option = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
        print(f'Option \n {updated_option}')
        general = updated_option['general']
        x_axis = updated_option['x_axis']
        y_axis = updated_option['y_axis']
        legend = updated_option['legend']
        overlay = updated_option['overlay']
        line = updated_option['line']
        bar = updated_option['bar']
        twin = updated_option['twin']
        
        plt.style.use(general['graph_style'])
        
        # 원본 보존을 위한 copy
        data = self._data.copy()
        
        # column 삭제 유무
        if general['drop_columns']:
            data.drop(general['drop_columns_name'], axis=general['drop_column_axis'], inplace=True)
            print(f"Deleted Column : {general['drop_columns']}\n{data}")
        
        # base64 Encoding을 위한 bytesIO
        __graphToBytes = BytesIO()

        # Draw Graph
        dfGraph = data.copy() if not general['flip'] else data.T.copy()
        fig, bargraph = plt.subplots(figsize=general['fig_size'])
        
        # print(dfGraph)
        
        # Bar Graph
        dfGraph.plot(
            kind = 'bar',
            stacked= bar['stack'],
            lw= bar['width'],
            color= bar['colors'],
            align= bar['align'],
            ax=bargraph,
        )
        
        plt.title(general['title'], loc='center')
        plt.xlim((x_axis['min'], x_axis['max']))
        plt.ylim((y_axis['min'], y_axis['max']))
        plt.xlabel(x_axis['label'])
        plt.ylabel(y_axis['label'])
        plt.xticks(rotation = x_axis['ticks'])
        plt.yticks(rotation = y_axis['ticks'])
        plt.legend(labels = data.columns if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
        # Twinx | Twiny
        linegraph = bargraph.twinx() if twin['twin'] is 'x' else bargraph.twiny()
        
        # Line Graph
        dfGraph.plot(
            marker= line['marker'],
            markersize= line['marker_size'],
            lw= line['width'],
            color=line['colors'],
            ax=linegraph,
        )
        
        plt.xlim((twin['x_min'], twin['x_max']))
        plt.ylim((twin['y_min'], twin['y_max']))
        plt.xlabel(twin['x_label'])
        plt.ylabel(twin['y_label'])
        plt.grid(visible=overlay['grid'])
        plt.legend(labels = data.columns if legend['labels'] is None else legend['labels'], loc=twin['legend'], fontsize=twin['legend_fontsize'])
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=200, bbox_inches='tight')
        plt.close()
        
        # Base64 encoding
        import base64
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,%s" % __convBase64
    
    
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
                    'drop_column_axis': 1, # Drop Column Axis  0 - horizental, 1 - vertical
                    'dpi': 200, # Graph Resolution  default = 200
                }
                ```
            x_axis (dict): 
                ```
                'x_axis': {
                    'label': None, # x axis label  str
                    'ticks': 45, # x label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            y_axis (dict):
                ```
                'y_axis': {
                    'label': None, # y axis label  str
                    'ticks': 0, # y label text rotate degree  -90 ~ 90
                    'min' : None, # limit low value
                    'max' : None, # limit high value
                }
                ```
            legend (dict): 
                ```
                'legend': {
                    'labels': None, # legend label  columns
                    'location': 'best', # legend location  best, left, center, right, upper [left, center, right], lower [left, center, right]
                    'fontsize': 7, # legend fontsize  int
                }
                ```
            overlay (dict): 
                ```
                'overlay': {
                    'grid': True, # graph in grid background  True, False
                    'axis': 0, # value axis  0 - horizental, 1 - vertical
                    'tight_layout': False, # graph layout margin  True, False
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
                    'colors': None, # Pie Colors  default following matplotlib colors    
                    'wedge_width': 0.5, # Pie To Donut width  default 0.5  float
                    'wedge_edge_color': None, # Pie To Donut color  default following matplotlib colors 
                    'explode': None # Pie piece Explode  tuple[float]     **tuple len == explode len**
                }
                ```
        """
        updated_option = self.optionUpdate(self.DEFAULT_OPTION.copy(), option)
        
        print(f'Option \n {updated_option}')
        general = updated_option['general']
        x_axis = updated_option['x_axis']
        y_axis = updated_option['y_axis']
        legend = updated_option['legend']
        overlay = updated_option['overlay']
        pie = updated_option['pie']
        
        plt.style.use(general['graph_style'])
        
        # 원본 보존을 위한 copy
        data = self._data.copy()
        
        # column 삭제 유무
        if general['drop_columns']:
            data.drop(general['drop_columns_name'], axis=general['drop_column_axis'], inplace=True)
            print(f"Deleted Column : {general['drop_columns_name']}\n{data}")
        
        # base64 Encoding을 위한 bytesIO
        __graphToBytes = BytesIO()

        # Draw Graph
        dfGraph = data.copy() if not general['flip'] else data.T.copy()
        plt.figure(figsize=general['fig_size'])
        
        # print(dfGraph)
        
        # Total Column for Pie Chart 100%
        dfGraph.loc['Total', :] = dfGraph[dfGraph.columns].sum()
        dfGraph = dfGraph.T
        
        dfGraph['Total'].plot(
            kind= 'pie',
            autopct= pie['autopct'],
            startangle= pie['startangle'],
            explode= pie['explode'],
            shadow= pie['shadow'],
            radius= pie['radius'],
            colors= pie['colors'],
            wedgeprops=dict(width=pie['wedge_width'], edgecolor=pie['wedge_edge_color'])
        )
        
        plt.title(general['title'], loc='center')
        plt.xlim((x_axis['min'], x_axis['max']))
        plt.ylim((y_axis['min'], y_axis['max']))
        plt.xlabel(x_axis['label'])
        plt.ylabel(y_axis['label'])
        plt.xticks(rotation = x_axis['ticks'])
        plt.yticks(rotation = y_axis['ticks'])
        plt.grid(visible=overlay['grid'])
        plt.legend(labels = data.columns if legend['labels'] is None else legend['labels'], loc=legend['location'], fontsize=legend['fontsize'])
        
        # Graph PNG Setting
        plt.savefig(__graphToBytes, format='png', dpi=200, bbox_inches='tight')
        plt.close()
        
        # Base64 encoding
        import base64
        __convBase64 = base64.b64encode(__graphToBytes.getvalue()).decode("utf-8").replace("\n", "")
        return "data:image/png;base64,%s" % __convBase64
