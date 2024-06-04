from fastapi import FastAPI
# from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from pydantic import BaseModel
# from fastapi.staticfiles import StaticFiles
# import json
# from texteditor.pythonPanel import panel
from module.loadData import loadJsonDataForSpreadSheet, loadJsonDataForGraph
from chart.chart import drawChart
import os, json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    
    graph = drawChart()
    # RestApi를 통해 json 을 받는 다는 가정으로 해당에 맞게 데이터 정제
    jsondata = open(f"{os.path.realpath('.')}/static/data/1715043362_pie.json", 'rb').read().decode('utf-8').replace('\\', '')
    jsondata = json.dumps(jsondata)
    
    jsondataList = eval(json.loads(jsondata))
    
    print(f'Lines : {len(jsondataList)}')
    graph.loadJsonDataToDict(jsondataList)
    
    # linechart = graph.line({})
    
    # barchart = graph.bar({
    #     # 'general' : {
    #     #     'graph_style': 'ggplot',
    #     #     # 'fig_size': (20, 5),
    #     #     'title': 'Status Day',
    #     #     'flip': False,
    #     #     # 'drop_columns': True,
    #     #     # 'drop_columns_name': ['NULL', '200', '404']
    #     # },
    #     # 'x_axis': {
    #     #     'label': 'Day',
    #     #     'ticks': 45,
    #     #     # 'min': 0,
    #     #     # 'max': 10
    #     # },
    #     # 'y_axis': {
    #     #     'label': 'Status',
    #     #     'ticks': 0,
    #     #     'min' : 0,
    #     #     # 'max' : 250000,
    #     # },
    #     # 'legend': {
    #     #     'location': 'best',
    #     #     'fontsize': 7,
    #     # },
    #     # 'bar': {
    #     #     'stack': True,
    #     #     # 'colors': ['r', 'g']
    #     # }
    # })
    
    # twinchart = graph.twin({
    #     # 'general' : {
    #     #     'graph_style': 'ggplot',
    #     #     # 'fig_size': (12, 5),
    #     #     'title': 'Status Day',
    #     #     'flip': False,
    #     #     # 'drop_columns': True,
    #     #     # 'drop_columns_name': ['NULL', '200', '404']
    #     # },
    #     # 'x_axis': {
    #     #     'label': 'Day',
    #     #     'ticks': 45,
    #     #     # 'min': 0,
    #     #     # 'max': 10
    #     # },
    #     # 'y_axis': {
    #     #     'label': 'Status',
    #     #     'ticks': 0,
    #     #     'min' : 0,
    #     #     # 'max' : 250000,
    #     # },
    #     # 'legend': {
    #     #     'location': 'upper left',
    #     #     'fontsize': 7,
    #     # },
    #     # 'line': {
    #     #     # 'colors': ['r', 'g']
    #     # },
    #     # 'bar': {
    #     #     'stack': True,
    #     #     'align': 'edge'
    #     #     # 'colors': ['r', 'g']
    #     # },
    #     # 'twin': {
    #     #     'twin': 'x'
    #     # }
    # })
    
    piechart = graph.pie({
        # 'general' : {
        #     'graph_style': 'ggplot',
        #     'fig_size': (12, 6),
        #     'title': 'Status Day',
        #     'flip': False,
        #     # 'drop_columns': True,
        #     # 'drop_columns_name': ['NULL', '200', '404']
        # },
        # 'x_axis': {
        #     'label': 'Day',
        #     'ticks': 45,
        #     'min': 0,
        #     # 'max': 10
        # },
        # 'y_axis': {
        #     'label': 'Status',
        #     'ticks': 0,
        #     'min' : 0,
        #     # 'max' : 250000,
        # },
        # 'legend': {
        #     'location': 'lower right',
        #     'fontsize': 7,
        # },
        # 'overlay': {
        #     'legend': True,
        # },
        # 'pie': {
        #     'autopct': '%.2f%%',
        #     'startangle': 10,
        #     'shadow': False,
        #     'radius': 0.8,
        #     # 'explode': [0.05, 0, 0, 0, 0, 0, 0, 0, 0],
        #     'arrow': True
        # }
    })
    
    resultImages = [piechart.replace('"', '')]
    return templates.TemplateResponse("index.html",{"request":request, "images": resultImages, "count": len(resultImages)})


@app.get("/editor", response_class=HTMLResponse)
async def home(request: Request):
    
    return templates.TemplateResponse("editor.html",{"request":request})



@app.get("/spreadsheet", response_class=HTMLResponse)
async def home(request: Request):
    data, columns = loadJsonDataForSpreadSheet("1715043362_19")
    
    return templates.TemplateResponse("spreadsheet.html",{"request":request, "data": data, "columns": columns})
