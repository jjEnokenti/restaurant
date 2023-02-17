import os

import dotenv

dotenv.load_dotenv()

__all__ = (
    'BaseConfig',
    'TestConfig'
)


class BaseConfig:
    USER = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    HOST = os.getenv("HOST")
    DB_NAME = os.getenv("DB_NAME")

    SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://" \
                              f"{USER}:{PASSWORD}@{HOST}/{DB_NAME}"


class TestConfig(BaseConfig):
    TEST_DB_NAME = os.getenv('TEST_DB_NAME')

    SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://" \
                              f"{BaseConfig.USER}:{BaseConfig.PASSWORD}@{BaseConfig.HOST}/{TEST_DB_NAME}"

