from fastapi import FastAPI
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chart.chart import drawChart

# uvicorn app:app --reload --port=3000


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
