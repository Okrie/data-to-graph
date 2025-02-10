from fastapi import FastAPI
# from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel
# from fastapi.staticfiles import StaticFiles
# import json
# from texteditor.pythonPanel import panel
from module.loadData import loadJsonDataForSpreadSheet, loadJsonDataForGraph
from chart.chart import drawChart
import os, json



templates = Jinja2Templates(directory="templates")

# app = FastAPI(docs_url="/documentation", redoc_url=None)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # jsondata = loadJsonDataForGraph("1715043362_19")
    
    graph = drawChart()
    # RestApi를 통해 json 을 받는 다는 가정으로 해당에 맞게 데이터 정제
    jsondata = open(f"{os.path.realpath('.')}/static/data/test_pie.json", 'rb').read().decode('utf-8').replace('\\', '')
    jsondata = json.dumps(jsondata)
    # jsondataList = jsondata.split('\n')[:-1]
    
    jsondataList = eval(json.loads(jsondata))
    
    print(f'Lines : {len(jsondataList)}')
    # 현재 json 데이터가 각 줄별로 데이터 날아 온 것처럼 합쳐져 있어 아래와 같이 나눠서 보냄
    # Response 내 "result" 항목이 하나라면 graph.loadJsonDataToDataframe(jsondata) 같이 사용
    # for i in range(len(jsondataList)):
    #     graph.loadJsonDataToDataframe(jsondataList[i])#, index='Malware Analysis')
    
    graph.loadJsonDataToDict(jsondataList)
    
    # linechart = graph.line({
    #     'general' : {
    #         'graph_style': 'ggplot',
    #         'fig_size': (20, 5),
    #         'title': 'Status Day',
    #         'flip': False,
    #         # 'drop_columns': True,
    #         # 'drop_columns_name': ['NULL', '200', '404']
    #     },
    #     'x_axis': {
    #         'label': 'Day',
    #         'ticks': 45,
    #         # 'min': 0,
    #         # 'max': 10
    #     },
    #     'y_axis': {
    #         'label': 'Status',
    #         'ticks': 0,
    #         'min' : 0,
    #         # 'max' : 250000,
    #     },
    #     'legend': {
    #         'location': 'best',
    #         'fontsize': 7,
    #     },
    #     'line': {
    #         # 'marker': None
    #         # 'colors': ['r', 'g']
    #     }
    # })
    
    # barchart = graph.bar({
    #     'general' : {
    #         'graph_style': 'ggplot',
    #         'fig_size': (20, 5),
    #         'title': 'Status Day',
    #         'flip': False,
    #         # 'drop_columns': True,
    #         # 'drop_columns_name': ['NULL', '200', '404']
    #     },
    #     'x_axis': {
    #         'label': 'Day',
    #         'ticks': 45,
    #         # 'min': 0,
    #         # 'max': 10
    #     },
    #     'y_axis': {
    #         'label': 'Status',
    #         'ticks': 0,
    #         'min' : 0,
    #         # 'max' : 250000,
    #     },
    #     'legend': {
    #         'location': 'best',
    #         'fontsize': 7,
    #     },
    #     'bar': {
    #         'stack': True,
    #         # 'colors': ['r', 'g']
    #     }
    # })
    
    # twinchart = graph.twin({
    #     'general' : {
    #         'graph_style': 'ggplot',
    #         'fig_size': (12, 5),
    #         'title': 'Status Day',
    #         'flip': False,
    #         # 'drop_columns': True,
    #         # 'drop_columns_name': ['NULL', '200', '404']
    #     },
    #     'x_axis': {
    #         'label': 'Day',
    #         'ticks': 45,
    #         # 'min': 0,
    #         # 'max': 10
    #     },
    #     'y_axis': {
    #         'label': 'Status',
    #         'ticks': 0,
    #         'min' : 0,
    #         # 'max' : 250000,
    #     },
    #     'legend': {
    #         'location': 'upper left',
    #         'fontsize': 7,
    #     },
    #     'line': {
    #         # 'colors': ['r', 'g']
    #     },
    #     'bar': {
    #         'stack': True,
    #         'align': 'edge'
    #         # 'colors': ['r', 'g']
    #     },
    #     'twin': {
    #         'twin': 'x'
    #     }
    # })
    
    piechart = graph.pie({
        'general' : {
            'graph_style': 'ggplot',
            'fig_size': (12, 6),
            'title': 'Status Day',
            'flip': False,
            # 'drop_columns': True,
            # 'drop_columns_name': ['NULL', '200', '404']
        },
        'x_axis': {
            'label': 'Day',
            'ticks': 45,
            'min': 0,
            # 'max': 10
        },
        'y_axis': {
            'label': 'Status',
            'ticks': 0,
            'min' : 0,
            # 'max' : 250000,
        },
        'legend': {
            'location': 'best',
            'fontsize': 7,
        },
        'overlay': {
            'legend': False,
        },
        'pie': {
            'autopct': '%.2f%%',
            'startangle': 10,
            'shadow': False,
            'radius': 0.8,
            # 'explode': [0.05, 0, 0, 0, 0, 0, 0, 0, 0],
            'arrow': True
        }
    }) 
    
    # graph.loadJsonDataToDataframe(jsondataList[1])
    # linechart = graph.drawGraph(kind='line', xticks=45, title="STATUS", xlabel='DAY', ylabel='COUNT')
    # twinchart = graph.drawGraph(kind='twin', twinx=True, stacked=False, xticks=45, xlabel='DAY', ylabel='COUNT', title='Bar Width Line')
    # barchart = graph.drawGraph(kind='bar', witdh=0.7, stacked=True, xticks=45, xlabel='DAY', ylabel='COUNT')
    # piechart = graph.drawGraph(kind='pie', dropcolumn=['NULL', '200'], figsize=(12, 5))
    resultImages = [piechart]
    return templates.TemplateResponse("index.html",{"request":request, "images": resultImages, "count": len(resultImages)})


# @app.get("/editor", response_class=HTMLResponse)
# async def home(request: Request):
    
#     return templates.TemplateResponse("editor.html",{"request":request})



# @app.get("/spreadsheet", response_class=HTMLResponse)
# async def home(request: Request):
#     data = loadJsonDataForSpreadSheet("1715043362_19")
    
#     return templates.TemplateResponse("spreadsheet.html",{"request":request, "data": data})
