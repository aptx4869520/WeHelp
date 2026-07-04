from typing import Annotated
import json
import ssl
import urllib.request

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



CHINESE_URL = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
ENGLISH_URL = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"


def load_hotels_from_urls():
    hotels_data = {}
    context = ssl._create_unverified_context()

    with urllib.request.urlopen(CHINESE_URL, context=context) as response:
        chinese_text = response.read().decode("utf-8")

    with urllib.request.urlopen(ENGLISH_URL, context=context) as response:
        english_text = response.read().decode("utf-8")

    chinese_data = json.loads(chinese_text)
    english_data = json.loads(english_text)

    chinese_hotels = chinese_data["list"]
    english_hotels = english_data["list"]

    english_dict = {}
    for english_hotel in english_hotels:
        hotel_source_id = english_hotel["_id"]
        english_dict[hotel_source_id] = english_hotel

    for index, chinese_hotel in enumerate(chinese_hotels, start=1):
        hotel_source_id = chinese_hotel["_id"]
        english_hotel = english_dict.get(hotel_source_id, {})

        hotels_data[index] = {
            "chinese_name": chinese_hotel["旅宿名稱"],
            "english_name": english_hotel.get("hotel name", ""),
            "phone": chinese_hotel["電話或手機號碼"]
        }

    return hotels_data

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

@app.get("/hotel/{hotel_id}")
def hotel(request: Request, hotel_id: int):
    hotels = load_hotels_from_urls()
    hotel_data = hotels.get(hotel_id)

    return templates.TemplateResponse(
        request=request,
        name="hotel.html",
        context={
            "hotel": hotel_data
        }
    )