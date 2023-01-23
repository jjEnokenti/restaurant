import os

import dotenv

dotenv.load_dotenv()


class BaseConfig:
    USER = os.environ.get("USER")
    PASSWORD = os.environ.get("PASSWORD")
    HOST = os.environ.get("HOST")
    DB_NAME = os.environ.get("DB_NAME")

    SQLALCHEMY_DATABASE_URL = f"postgresql://" \
                              f"{USER}:{PASSWORD}@{HOST}/{DB_NAME}"


class TestConfig:
    USER = os.environ.get("TEST_USER")
    PASSWORD = os.environ.get("TEST_PASSWORD")
    HOST = os.environ.get("TEST_HOST")
    DB_NAME = os.environ.get("TEST_DB_NAME")

    TEST_SQLALCHEMY_DATABASE_URL = f"postgresql://" \
                                   f"{USER}:{PASSWORD}@{HOST}/{DB_NAME}"
