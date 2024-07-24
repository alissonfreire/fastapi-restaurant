from typing import List

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user_schema import UserCreateInput, UserUpdateInput


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_users(self) -> List[User]:
        return self.session.query(User).all()

    def create_user(self, data: UserCreateInput) -> User:
        user = User(**data.dict())
        return self.__save_and_refresh(user, True)

    def get_user_by_id(self, user_id: int) -> User | None:
        return self.get_user_by({'id': user_id})

    def get_user_by(self, params: dict) -> User | None:
        return self.session.query(User).filter_by(**params).first()

    def update_user(self, user_id: int, data: UserUpdateInput) -> User | None:
        user = self.get_user_by_id(user_id)

        if user is None:
            return None

        for key, value in data.dict(exclude_unset=True).items():
            setattr(user, key, value)

        return self.__save_and_refresh(user)

    def delete_user(self, user_id: int) -> True:
        user = self.get_user_by_id(user_id)

        if user is None:
            return None

        self.session.delete(user)
        self.session.commit()

        return True

    def __save_and_refresh(self, user: User, add=False) -> User:
        if add:
            self.session.add(user)

        self.session.commit()
        self.session.refresh(user)
        return user
