import pytest
from factories import UserFactory

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreateInput, UserUpdateInput


@pytest.fixture
def user_repo(session):
    return UserRepository(session=session)


def create_many_users(session, number=5):
    users = UserFactory.create_batch(number, password='123456789')

    session.bulk_save_objects(users)
    session.commit()

    return users


def test_should_create_a_user_with_valid_data(session, user_repo):
    # arrange
    data = UserCreateInput(
        username='test user', email='user@email.com', password='123456789'
    )

    # act
    user_repo.create_user(data)

    # assert
    created_user = session.query(User).filter_by(username='test user').first()

    assert created_user is not None
    assert type(created_user.id) is int
    assert created_user.username == data.username
    assert created_user.email == data.email
    assert created_user.password == data.password


def test_should_return_all_users(session, user_repo):
    # arrange
    NUM_USERS = 5
    create_many_users(session, number=NUM_USERS)

    # act
    returned_users = user_repo.get_all_users()

    # assert
    assert len(returned_users) == NUM_USERS

    for user in returned_users:
        assert user.id is not None
        assert user.username.startswith('test')


def test_should_return_user_by_id(user, user_repo):
    # arrange
    # act

    returned_user = user_repo.get_user_by_id(user.id)

    # assert
    assert returned_user is not None
    assert returned_user.id == user.id


def test_should_update_a_user_with_valid_data(user, user_repo):
    # arrange
    data = UserUpdateInput(
        username='test update user', email='update_user@email.com'
    )

    # act
    returned_user = user_repo.update_user(user.id, data)

    # assert
    assert returned_user.id == user.id
    assert returned_user.username == 'test update user'
    assert returned_user.email == 'update_user@email.com'


def test_should_returns_none_on_update_nonexistent_use(user_repo):
    # arrange
    random_user_id = 1000
    data = UserUpdateInput(
        username='test update user', email='update_user@email.com'
    )

    # act
    return_value = user_repo.update_user(random_user_id, data)

    # assert
    assert return_value is None


def test_should_delete_a_user_by_id(session, user, user_repo):
    # arrange
    # act
    return_value = user_repo.delete_user(user.id)

    # assert
    assert return_value

    delete_user = session.query(User).filter_by(id=user.id).first()
    assert delete_user is None


def test_should_returns_none_on_delete_nonexistent_use(user_repo):
    # arrange
    random_user_id = 1000
    # act
    return_value = user_repo.delete_user(random_user_id)

    # assert
    assert return_value is None
