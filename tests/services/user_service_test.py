import pytest
from factories import UserFactory

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import (
    UserCreateInput,
    UserLoginInput,
    UserUpdateInput,
)
from app.security import Security
from app.services.user_service import UserService


@pytest.fixture
def user_service(session):
    return UserService(
        user_repo=UserRepository(session=session), security=Security
    )


def create_many_users(session, number=5):
    users = UserFactory.create_batch(number)

    session.bulk_save_objects(users)
    session.commit()

    return users


def test_should_register_a_user_with_valid_data(session, user_service):
    # arrange
    data = UserCreateInput(
        username='test user', email='user@email.com', password='123456789'
    )

    # act
    user, token = user_service.register_user(data)

    # assert
    created_user = session.query(User).filter_by(username='test user').first()

    assert created_user is not None
    assert type(created_user.id) is int
    assert created_user.id == user.id
    assert created_user.username == data.username
    assert created_user.email == data.email
    assert created_user.password == data.password
    assert created_user.password != '123456789'

    assert token is not None


def test_should_login_a_valid_user(user, user_service):
    # arrange
    data = UserLoginInput(email=user.email, password='123456789')
    # act
    logged_user, token = user_service.login_user(data)

    # assert
    assert logged_user is not None
    assert logged_user.id == user.id
    assert logged_user.email == user.email
    assert token is not None


def test_dont_login_user_with_invalid_password(user, user_service):
    # arrange
    data = UserLoginInput(email=user.email, password='1111111111')
    # act
    result = user_service.login_user(data)

    # assert
    assert not result


def test_dont_login_a_noexistent_user_with_invalid_email(user_service):
    # arrange
    data = UserLoginInput(email='noexistent@email.com', password='1111111111')
    # act
    result = user_service.login_user(data)

    # assert
    assert not result


def test_should_return_a_user_from_a_valid_token(user, user_service):
    # arrange
    data = UserLoginInput(email=user.email, password='123456789')
    _logged_user, token = user_service.login_user(data)

    # act
    user_from_token = user_service.get_user_from_token(token)

    # assert
    assert user_from_token is not None
    assert user_from_token.id == user.id
    assert user_from_token.email == user.email


def test_should_return_none_user_from_a_ivalid_token(user, user_service):
    # arrange
    token = 'invalid-access-token'

    # act
    user_from_token = user_service.get_user_from_token(token)

    # assert
    assert user_from_token is None


def test_should_return_all_users(session, user_service):
    # arrange
    NUM_USERS = 5
    create_many_users(session, number=NUM_USERS)

    # act
    returned_users = user_service.get_all_users()

    # assert
    assert len(returned_users) == NUM_USERS

    for user in returned_users:
        assert user.id is not None
        assert user.username.startswith('test')


def test_should_return_user_by_id(user, user_service):
    # arrange
    # act

    returned_user = user_service.get_user_by_id(user.id)

    # assert
    assert returned_user is not None
    assert returned_user.id == user.id


def test_should_update_a_user_with_valid_data(user, user_service):
    # arrange
    data = UserUpdateInput(
        username='test update user', email='update_user@email.com'
    )

    # act
    returned_user = user_service.update_user(user.id, data)

    # assert
    assert returned_user.id == user.id
    assert returned_user.username == 'test update user'
    assert returned_user.email == 'update_user@email.com'


def test_should_returns_none_on_update_nonexistent_use(user_service):
    # arrange
    random_user_id = 1000
    data = UserUpdateInput(
        username='test update user', email='update_user@email.com'
    )

    # act
    return_value = user_service.update_user(random_user_id, data)

    # assert
    assert return_value is None


def test_should_delete_a_user_by_id(session, user, user_service):
    # arrange
    # act
    return_value = user_service.delete_user(user.id)

    # assert
    assert return_value

    delete_user = session.query(User).filter_by(id=user.id).first()
    assert delete_user is None


def test_should_returns_none_on_delete_nonexistent_use(user_service):
    # arrange
    random_user_id = 1000
    # act
    return_value = user_service.delete_user(random_user_id)

    # assert
    assert return_value is None
