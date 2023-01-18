import os

import dotenv


dotenv.load_dotenv()


class Config:

    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")
    HOST = os.environ.get("HOST")
    DB_NAME = os.environ.get("DB_NAME")

    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://" \
                              f"{USER}:{PASSWORD}@{HOST}:5432/{DB_NAME}"