from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from database import get_db_connection

from typing import Any, cast

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key="week6-secret-key"
)

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
    member_id = request.session.get("member_id")
    member_name = request.session.get("member_name")

    if member_id is None:
        return RedirectResponse(
            url="/",
            status_code=303
        )

    return templates.TemplateResponse(
        request,
        "member.html",
        {
            "name": member_name
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

@app.post("/signup")
async def signup(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        check_email_sql = """
            SELECT id
            FROM member
            WHERE email = %s
        """

        cursor.execute(check_email_sql, (email,))
        existing_member = cursor.fetchone()

        if existing_member is not None:
            return RedirectResponse(
                url="/ohoh?msg=重複的電子郵件 ",
                status_code=303
            )

        insert_member_sql = """
            INSERT INTO member (name, email, password)
            VALUES (%s, %s, %s)
        """

        cursor.execute(
            insert_member_sql,
            (name, email, password)
        )

        connection.commit()

        return RedirectResponse(
            url="/",
            status_code=303
        )

    except Exception as error:
        print("Signup error:", error)

        return RedirectResponse(
            url="/ohoh?msg=系統發生錯誤",
            status_code=303
        )

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()            

@app.post("/signin")
async def signin(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        signin_sql = """
            SELECT id, name, email
            FROM member
            WHERE email = %s
            AND password = %s
        """

        cursor.execute(
            signin_sql,
            (email, password)
        )

        member = cursor.fetchone()

        if member is None:
            return RedirectResponse(
                url="/ohoh?msg=電子郵件或密碼輸入錯誤",
                status_code=303
            )
        
        member = cast(dict[str, Any], member)

        request.session["member_id"] = member["id"]
        request.session["member_name"] = member["name"]
        request.session["member_email"] = member["email"]

        return RedirectResponse(
            url="/member",
            status_code=303
        )

    except Exception as error:
        print("Signin error:", error)

        return RedirectResponse(
            url="/ohoh?msg=系統發生錯誤",
            status_code=303
        )

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()            
