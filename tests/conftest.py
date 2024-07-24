import os

import pytest
from factories import UserFactory
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.config.database import get_session, table_registry
from app.helpers import load_env
from app.main import app


@pytest.fixture(scope='session', autouse=True)
def _set_test_env():
    os.environ['ENV'] = 'test'

    load_env()


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


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
    user = UserFactory()

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = '123456789'

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/login',
        json={
            'email': user.email,
            'password': user.clean_password,
        },
    )
    return response.json()['data']['access_token']
