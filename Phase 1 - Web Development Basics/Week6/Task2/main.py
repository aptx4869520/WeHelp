from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from database import get_db_connection


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