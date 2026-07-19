from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request, 
        "index.html"
    )

@app.get("/member", response_class=HTMLResponse)
async def member_page(request: Request):    
    return templates.TemplateResponse(
        request,
        "member.html",
        {
            "name": "測試會員"
        }
    )

@app.get("/ohoh", response_class=HTMLResponse)
async def error_page(request: Request, msg: str):
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "message": msg
        }
    )