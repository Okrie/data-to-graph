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




templates = Jinja2Templates(directory="templates")

# app = FastAPI(docs_url="/documentation", redoc_url=None)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # jsondata = loadJsonDataForGraph("1715043362_19")
    
    data = drawChart()
    # RestApi를 통해 json 을 받는 다는 가정으로 해당에 맞게 데이터 정제
    import os
    jsondata = open(f'{os.path.realpath('.')}/static/data/1715043362_19.json', 'rb')
    jsondata = jsondata.read().decode('utf-8')
    jsondataList = jsondata.split('\n')[:-1]
    
    print(f'Lines : {len(jsondataList)}')
    for i in range(len(jsondataList)):
        data.loadJsonDataToDataframe(jsondataList[i])
    
    graph = drawChart(jsondata)
    
    linechart = graph.drawGraph()
    twinchart = graph.drawGraph(graphType='twin')
    barchart = graph.drawGraph(graphType='bar')
    piechart = graph.drawGraph(graphType='pie')
    resultImages = [linechart, barchart, twinchart, piechart]
    # print(readLogData("access.log"))
    return templates.TemplateResponse("index.html",{"request":request, "images": resultImages, "count": len(resultImages)})


# @app.get("/editor", response_class=HTMLResponse)
# async def home(request: Request):
    
#     return templates.TemplateResponse("editor.html",{"request":request})



# @app.get("/spreadsheet", response_class=HTMLResponse)
# async def home(request: Request):
#     data = loadJsonDataForSpreadSheet("1715043362_19")
    
#     return templates.TemplateResponse("spreadsheet.html",{"request":request, "data": data})
