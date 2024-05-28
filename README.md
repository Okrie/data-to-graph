# Chart View
- python 에서 fastapi, jinja2 를 사용하여 원시데이터를 정제하여 도표로 출력

1. pip install requirements
```
pip install -r requirements.txt
```    
     
     
2. activate env    
         

3. run fastapi
```
uvicorn app:app --reload --port=3000
```    


4. connect localhost:3000/
5. push 'submit' button
6. Done     


-----------------------------------------
## OPTION
```python
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
        'dpi': 150,             # Graph Resolution              default = 150
        'img_width': 700        # Image px                      default = 700
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
        'width': 1,             # Bar Width                     float over 0
        'colors': __SPLUNK_BASE_COLOR_MAP['categorical_2'], # Bar Colors    default on SPLUNK color map
        'stack': True,          # Bar values Stacked            True, False
        'align': 'center',          # Bar align                     center, edge
    },
    'twin': {
        'twin': 'x',            # Twin Axis                     default x  y
        'x_label': '',          # Twin x label                  str
        'y_label': '',          # Twin y label                  str
        'x_min': None,          # Twin x min value              float
        'x_max': None,          # Twin x max value              float
        'y_min': None,          # Twin y min value              float
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

```
