import os

import pytest

from app.helpers import load_env


@pytest.fixture(scope='session', autouse=True)
def _set_test_env():
    os.environ['ENV'] = 'test'

    load_env()
