import os

from dotenv import find_dotenv, load_dotenv


def load_env():
    load_dotenv(find_dotenv())

    if os.getenv('ENV', 'dev') == 'test':
        load_dotenv(find_dotenv('.env.testing'), override=True)
