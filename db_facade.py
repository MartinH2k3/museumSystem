import psycopg2
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = ".env"
        case_sensitive = True

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str


settings = Settings()


def get_connection():
    return psycopg2.connect(
        host=settings.DATABASE_HOST,
        port=settings.DATABASE_PORT,
        database=settings.DATABASE_NAME,
        user=settings.DATABASE_USER,
        password=settings.DATABASE_PASSWORD,
    )


def select_query(query: str) -> list: # returns list of tuples
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return result
    except Exception as e:
        cursor.close()
        connection.close()
        return "error: " + str(e)


def insert_query(query: str) -> str:  # returns if the query was successful
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        for notice in connection.notices:
            print(notice)
        return "success"
    except Exception as e:
        cursor.close()
        connection.close()
        return "error: " + str(e)

