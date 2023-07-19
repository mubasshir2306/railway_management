from psycopg2 import connect, Error
from dotenv import load_dotenv
from os import environ as env

load_dotenv()


def get_connection():
    connection = None

    try:
        connection = connect(
            host=env.get("HOST_NAME"),
            port=env.get("PORT_NAME"),
            user=env.get("USER_NAME"),
            password=env.get("PASSWORD"),
            database=env.get("DATABASE_NAME")
        )

    except Error as e:
        print(f"Error '{e}' occurred while attempting to connect to the database.")

    return connection
