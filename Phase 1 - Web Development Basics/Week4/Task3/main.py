from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(
    SessionMiddleware, 
    secret_key="your-secret-key"
)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

@app.post("/login")
def login(
    request: Request,
    email: Annotated[str | None, Form()] = None,
    password: Annotated[str | None, Form()] = None,
    agree: Annotated[str | None, Form()] = None
):
    if agree is None:
        return RedirectResponse(
            url="/ohoh?message=請勾選同意條款",
            status_code=303
        )

    if email == "abc@abc.com" and password == "abc":
        request.session["LOGGED-IN"] = True

        return RedirectResponse(
            url="/member",
            status_code=303
        )
    
    if email is None or password is None or email == "" or password == "":
        return RedirectResponse(
            url="/ohoh?message=請輸入信箱和密碼",
            status_code=303
        )

    return RedirectResponse(
        url="/ohoh?message=帳號、或密碼輸入錯誤",
        status_code=303
    )

@app.get("/logout")
def logout(request: Request):
    request.session["LOGGED-IN"] = False
    return RedirectResponse(
        url="/",
        status_code=303
    )

@app.get("/member")
def member(request: Request):
    is_logged_in = request.session.get("LOGGED-IN", False)

    if not is_logged_in:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="member.html",
        context={}
    )

@app.get("/ohoh")
def ohoh(request: Request, message: str):
    return templates.TemplateResponse(
        request=request,
        name="ohoh.html",
        context={
            "message": message
        }
    )