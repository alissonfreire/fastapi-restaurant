import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.helpers import load_env

load_env()

SQLALCHEMY_DATABASE_URL = os.get_env('DATABASE_URL')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
