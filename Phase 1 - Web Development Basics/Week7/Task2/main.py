import hashlib
import secrets

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.middleware.sessions import SessionMiddleware

from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

from database import get_db_connection

from pydantic import BaseModel
from typing import Any, cast

mcp = FastMCP(
    name="Testing Message Website"
)

@mcp.tool(
    name="Create Message",
    description=(
        "Create a new message in "
        "Testing Message Website."
    )
)
async def create_message_tool(
    content: str
) -> dict[str, bool]:
    headers = get_http_headers()

    authorization = headers.get("authorization")

    token = get_bearer_token(authorization)

    if token is None:
        return {
            "error": True
        }

    content = content.strip()

    if content == "":
        return {
            "error": True
        }

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        find_member_sql = """
            SELECT id
            FROM member
            WHERE token = %s
        """

        cursor.execute(
            find_member_sql,
            (token,)
        )

        member = cursor.fetchone()

        if member is None:
            return {
                "error": True
            }

        member = cast(dict[str, Any], member)

        insert_message_sql = """
            INSERT INTO message (member_id, content)
            VALUES (%s, %s)
        """

        cursor.execute(
            insert_message_sql,
            (
                member["id"],
                content
            )
        )

        connection.commit()

        return {
            "ok": True
        }

    except Exception as error:
        print("MCP create message error:", error)

        if connection is not None:
            connection.rollback()

        return {
            "error": True
        }

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()

mcp_app = mcp.http_app(path="/")

app = FastAPI(
    lifespan=mcp_app.lifespan
)

app.add_middleware(
    SessionMiddleware,
    secret_key="week6-secret-key"
)

app.mount("/mcp", mcp_app)

def generate_access_token(member_id: int) -> str:
    random_value = secrets.token_hex(32)

    raw_value = f"{member_id}:{random_value}"

    token = hashlib.sha256(
        raw_value.encode("utf-8")
    ).hexdigest()

    return token

def get_bearer_token(
    authorization: str | None
) -> str | None:
    if authorization is None:
        return None

    scheme, separator, token = authorization.partition(" ")

    if separator == "":
        return None

    if scheme.lower() != "bearer":
        return None

    token = token.strip()

    if token == "":
        return None

    return token

class MessageCreate(BaseModel):
    content: str

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
        request=request,
        name="member.html",
        context={
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

@app.get("/signout")
async def signout(request: Request):
    request.session.clear()
    return RedirectResponse(
        url="/",
        status_code=303
    )

@app.put("/api/token")
async def create_access_token(
    request: Request
):
    member_id = request.session.get("member_id")

    if member_id is None:
        return {
            "error": True
        }

    token = generate_access_token(member_id)

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        update_token_sql = """
            UPDATE member
            SET token = %s
            WHERE id = %s
        """

        cursor.execute(
            update_token_sql,
            (
                token,
                member_id
            )
        )

        if cursor.rowcount == 0:
            return {
                "error": True
            }

        connection.commit()

        return {
            "ok": True,
            "token": token
        }

    except Exception as error:
        print("Create access token error:", error)

        if connection is not None:
            connection.rollback()

        return {
            "error": True
        }

    finally:
        if cursor is not None:
            cursor.close()

        if (
            connection is not None
            and connection.is_connected()
        ):
            connection.close()

@app.post("/api/message")
async def create_message(
    request: Request,
    data: MessageCreate
):
    member_id = request.session.get("member_id")

    if member_id is None:
        return {
            "error": True
        }

    content = data.content.strip()

    if content == "":
        return {
            "error": True
        }

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            INSERT INTO message (member_id, content)
            VALUES (%s, %s)
        """

        cursor.execute(
            sql,
            (member_id, content)
        )

        connection.commit()

        return {
            "ok": True
        }

    except Exception as error:
        print("Create message error:", error)

        return {
            "error": True
        }

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

@app.get("/api/message")
async def get_messages(request: Request):
    member_id = request.session.get("member_id")

    if member_id is None:
        return {
            "error": True
        }

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        sql = """
            SELECT
                message.id,
                member.name,
                message.content,
                message.member_id
            FROM message
            INNER JOIN member
                ON message.member_id = member.id
            ORDER BY message.time DESC
        """

        cursor.execute(sql)
        rows = cursor.fetchall()
        rows = cast(list[dict[str, Any]], rows)

        messages = []

        for row in rows:
            messages.append({
                "id": row["id"],
                "name": row["name"],
                "content": row["content"],
                "self": row["member_id"] == member_id
            })

        return {
            "ok": True,
            "data": messages
        }

    except Exception as error:
        print("Get messages error:", error)

        return {
            "error": True
        }

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

@app.delete("/api/message/{message_id}")
async def delete_message(
    request: Request,
    message_id: int
):
    member_id = request.session.get("member_id")

    if member_id is None:
        return {
            "error": True
        }

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        sql = """
            DELETE FROM message
            WHERE id = %s
            AND member_id = %s
        """

        cursor.execute(
            sql,
            (message_id, member_id)
        )

        if cursor.rowcount == 0:
            return {
                "error": True
            }

        connection.commit()

        return {
            "ok": True
        }

    except Exception as error:
        print("Delete message error:", error)

        return {
            "error": True
        }

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
