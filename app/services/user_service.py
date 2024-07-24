from typing import List, Tuple

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (
    UserCreateInput,
    UserLoginInput,
    UserUpdateInput,
)
from app.security import Security


class UserService:
    def __init__(self, session: Session):
        self.user_repo = UserRepository(session=session)
        self.security = Security()

    def get_all_users(self) -> List[User]:
        return self.user_repo.get_all_users()

    def register_user(self, data: UserCreateInput) -> Tuple[User, str]:
        data.password = self.security.get_password_hash(data.password)
        user = self.user_repo.create_user(data)
        access_token = self.security.create_access_token(data={'sub': user.id})

        return user, access_token

    def login_user(self, data: UserLoginInput) -> Tuple[User, str] | False:
        user = self.user_repo.get_user_by({'email': data.email})

        # this step is necessary to prevent user enumeration attacks
        password_hash = self.security.wrong_password_hash()

        if user:
            password_hash = user.password

        is_valid = self.security.verify_password(data.password, password_hash)

        if not is_valid:
            return False

        access_token = self.security.create_access_token(data={'sub': user.id})

        return user, access_token

    def get_user_from_token(self, access_token: str) -> User | None:
        payload = Security.decode_access_token(access_token)

        if type(payload) is not dict:
            return None

        user = self.get_user_by_id(payload.get('sub'))

        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.user_repo.get_user_by_id(user_id)

    def update_user(self, user_id: int, data: UserUpdateInput) -> User | None:
        return self.user_repo.update_user(user_id, data)

    def delete_user(self, user_id: int) -> True:
        return self.user_repo.delete_user(user_id)
