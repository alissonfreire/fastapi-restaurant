import factory

from app.models.user import User
from app.security import Security


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = Security.get_password_hash('123456789')
