from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chart.chart import drawChart
from texteditor.pythonPanel import panel
from module.loadData import loadJsonDataForSpreadSheet
import json



templates = Jinja2Templates(directory="templates")

# app = FastAPI(docs_url="/documentation", redoc_url=None)
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    graph = drawChart("1715043362_19")
    linechart = graph.drawGraph()
    twinchart = graph.drawGraph(graphType='twin')
    barchart = graph.drawGraph(graphType='bar')
    piechart = graph.drawGraph(graphType='pie')
    resultImages = [linechart, barchart, twinchart, piechart]
    return templates.TemplateResponse("index.html",{"request":request, "images": resultImages, "count": len(resultImages)})


@app.get("/editor", response_class=HTMLResponse)
async def home(request: Request):
    
    return templates.TemplateResponse("editor.html",{"request":request})



@app.get("/spreadsheet", response_class=HTMLResponse)
async def home(request: Request):
    data = loadJsonDataForSpreadSheet("1715043362_19")
    data = json.dumps(data)
    # data = f"<script> var data = {data}; consol.log(data); </script>"
    return templates.TemplateResponse("spreadsheet.html",{"request":request, "data": data})
