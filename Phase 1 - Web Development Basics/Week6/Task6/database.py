import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="ddmpkdanny98",
        database="website"
    )

    return connection