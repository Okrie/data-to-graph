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
import os



templates = Jinja2Templates(directory="templates")

# app = FastAPI(docs_url="/documentation", redoc_url=None)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # jsondata = loadJsonDataForGraph("1715043362_19")
    
    graph = drawChart()
    # RestApi를 통해 json 을 받는 다는 가정으로 해당에 맞게 데이터 정제
    jsondata = open(f"{os.path.realpath('.')}/static/data/1715043362_19.json", 'rb')
    jsondata = jsondata.read().decode('utf-8')
    jsondataList = jsondata.split('\n')[:-1]
    
    print(f'Lines : {len(jsondataList)}')
    # 현재 json 데이터가 각 줄별로 데이터 날아 온 것처럼 합쳐져 있어 아래와 같이 나눠서 보냄
    # Response 내 "result" 항목이 하나라면 graph.loadJsonDataToDataframe(jsondata) 같이 사용
    for i in range(len(jsondataList)):
        graph.loadJsonDataToDataframe(jsondataList[i])
    
    linechart = graph.drawGraph(kind='line', xticks=45, label='Status', title="STATUS", xlabel='DAY', ylabel='COUNT')
    twinchart = graph.drawGraph(kind='twin', twinx=True, stacked=True, xticks=45, xlabel='DAY', ylabel='COUNT', title='Bar Width Line')
    barchart = graph.drawGraph(kind='bar', witdh=0.7, stacked=True, xticks=45, xlabel='DAY', ylabel='COUNT')
    piechart = graph.drawGraph(kind='pie', dropcolumn=['NULL', '200'], label='Status', figsize=(14, 5))
    resultImages = [linechart, barchart, twinchart, piechart]
    return templates.TemplateResponse("index.html",{"request":request, "images": resultImages, "count": len(resultImages)})


# @app.get("/editor", response_class=HTMLResponse)
# async def home(request: Request):
    
#     return templates.TemplateResponse("editor.html",{"request":request})



# @app.get("/spreadsheet", response_class=HTMLResponse)
# async def home(request: Request):
#     data = loadJsonDataForSpreadSheet("1715043362_19")
    
#     return templates.TemplateResponse("spreadsheet.html",{"request":request, "data": data})
