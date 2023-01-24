import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from run import app
from menu_app.dependences import get_db
from menu_app.core.init_db import Base
from menu_app.configs.config import TestConfig


engine = create_engine(TestConfig.SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def test_client():
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    del app.dependency_overrides[get_db]
