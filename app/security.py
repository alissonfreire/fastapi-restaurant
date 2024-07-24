import os
from datetime import datetime, timedelta

from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30')
)


class Security:
    pwd_context = PasswordHash.recommended()

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({'exp': expire})
        encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> dict | None:
        try:
            payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except DecodeError:
            return None

    @staticmethod
    def get_password_hash(password: str) -> str:
        return Security.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> str:
        return Security.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def wrong_password_hash() -> str:
        return os.getenv('WRONG_PASSWORD_HASH')
