import psycopg2

import settings


def connect():
    return psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host="localhost",
        port=5432
    )


connection = connect()
