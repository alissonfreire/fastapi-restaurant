import os

import pytest
from factories import UserFactory
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.config.database import table_registry
from app.helpers import load_env


@pytest.fixture(scope='session', autouse=True)
def _set_test_env():
    os.environ['ENV'] = 'test'

    load_env()


@pytest.fixture
def session():
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = UserFactory(password='123456789')

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
