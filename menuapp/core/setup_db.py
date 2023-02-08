from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from menuapp.configs.config import BaseConfig

db = create_engine(BaseConfig.SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)
