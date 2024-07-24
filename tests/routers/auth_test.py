from http import HTTPStatus


def test_should_register_a_user_with_valid_data(client):
    # arrange
    data = {
        'username': 'user',
        'email': 'user@example.com',
        'password': 'secretpass',
    }

    # act
    response = client.post('/auth/register', json=data)

    # assert
    assert response.status_code == HTTPStatus.CREATED

    response_body = response.json()
    assert response_body.get('status') == 'success'

    response_data = response_body.get('data')
    assert type(response_data) is dict

    assert 'user' in response_data
    user = response_data.get('user')

    assert type(user.get('id')) is int
    assert user.get('username') == data['username']
    assert user.get('email') == data['email']

    assert 'access_token' in response_data
    assert type(response_data.get('access_token')) is str


def test_dont_register_a_user_with_invalid_data(client):
    # arrange
    data = {
        'username': 1,
        'email': 'invalid-email',
    }

    # act
    response = client.post('/auth/register', json=data)

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    response_body = response.json()
    assert response_body.get('status') == 'fail'
    assert response_body.get('message') == 'validation error'

    response_errors = response_body.get('errors')
    assert type(response_errors) is list

    assert response_errors == [
        {
            'loc': ['body', 'username'],
            'msg': 'ensure this value has at least 3 characters',
            'type': 'value_error.any_str.min_length',
            'ctx': {'limit_value': 3},
        },
        {
            'loc': ['body', 'email'],
            'msg': 'value is not a valid email address',
            'type': 'value_error.email',
        },
        {
            'loc': ['body', 'password'],
            'msg': 'field required',
            'type': 'value_error.missing',
        },
    ]


def test_should_login_a_user_with_invalid_data(client):
    # arrange
    data = {
        'email': 'invalid-email',
    }

    # act
    response = client.post('/auth/login', json=data)

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    response_body = response.json()
    assert response_body.get('status') == 'fail'
    assert response_body.get('message') == 'validation error'

    response_errors = response_body.get('errors')
    assert type(response_errors) is list

    assert response_errors == [
        {
            'loc': [
                'body',
                'email',
            ],
            'msg': 'value is not a valid email address',
            'type': 'value_error.email',
        },
        {
            'loc': [
                'body',
                'password',
            ],
            'msg': 'field required',
            'type': 'value_error.missing',
        },
    ]


def test_should_login_a_user_with_valid_data(client, user):
    # arrange
    data = {
        'email': user.email,
        'password': user.clean_password,
    }

    # act
    response = client.post('/auth/login', json=data)

    # assert
    assert response.status_code == HTTPStatus.OK

    response_body = response.json()
    assert response_body.get('status') == 'success'

    response_data = response_body.get('data')
    assert type(response_data) is dict

    assert 'user' in response_data
    logged_user = response_data.get('user')

    assert type(logged_user.get('id')) is int
    assert logged_user.get('id') == user.id
    assert logged_user.get('email') == data['email']

    assert 'access_token' in response_data
    assert type(response_data.get('access_token')) is str


def test_dont_login_a_user_with_invalid_password(client, user):
    # arrange
    data = {
        'email': user.email,
        'password': 'wrong-password',
    }

    # act
    response = client.post('/auth/login', json=data)

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response_body = response.json()
    assert response_body.get('status') == 'fail'
    assert response_body.get('message') == 'unauthorized error'

    response_errors = response_body.get('errors')
    assert type(response_errors) is dict

    assert response_errors == {}


def test_dont_login_a_user_with_nonextistent_user_email(client):
    # arrange
    data = {
        'email': 'nonextistent@email.com',
        'password': '123456789',
    }

    # act
    response = client.post('/auth/login', json=data)

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response_body = response.json()
    assert response_body.get('status') == 'fail'
    assert response_body.get('message') == 'unauthorized error'

    response_errors = response_body.get('errors')
    assert type(response_errors) is dict

    assert response_errors == {}


def test_should_return_logged_user(client, user, token):
    # arrange
    # act
    response = client.get(
        '/auth/me', headers={'Authorization': f'Bearer {token}'}
    )

    # assert
    assert response.status_code == HTTPStatus.OK

    response_body = response.json()
    assert response_body.get('status') == 'success'

    response_data = response_body.get('data')
    assert type(response_data) is dict

    assert 'user' in response_data
    logged_user = response_data.get('user')

    assert type(logged_user.get('id')) is int
    assert logged_user.get('id') == user.id
    assert logged_user.get('email') == user.email


def test_dont_return_user_with_invalid_token(client):
    # arrange
    token = 'invali-token'

    # act
    response = client.get(
        '/auth/me', headers={'Authorization': f'Bearer {token}'}
    )

    # assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    response_body = response.json()
    assert response_body.get('status') == 'fail'
    assert response_body.get('message') == 'unauthorized error'

    response_errors = response_body.get('errors')
    assert type(response_errors) is dict

    assert response_errors == {}
