from app.security import Security


def test_should_be_hash_a_password():
    # arrange
    raw_password = '123456789'
    # act
    hashed_password = Security.get_password_hash(raw_password)

    # assert
    assert type(hashed_password) is str
    assert hashed_password != raw_password


def test_should_be_returns_true_when_verify_a_valid_hashed_password():
    # arrange
    raw_password = '123456789'
    hashed_password = Security.get_password_hash(raw_password)

    # act
    result = Security.verify_password(raw_password, hashed_password)

    # assert
    assert result


def test_should_be_returns_false_when_verify_a_invalid_hashed_password():
    # arrange
    raw_password = '123456789'
    hashed_password = Security.get_password_hash(raw_password)

    # act
    result = Security.verify_password('invalid_password', hashed_password)

    # assert
    assert not result


def test_should_be_returns_valid_access_token():
    # arrange
    data = {'sub': '123456789'}

    # act
    access_token = Security.create_access_token(data)

    # assert
    assert type(access_token) is str


def test_should_be_decode_a_valid_access_token():
    # arrange
    data = {'sub': '123456789'}
    access_token = Security.create_access_token(data)

    # act
    payload = Security.decode_access_token(access_token)

    # assert
    assert type(payload) is dict
    assert 'sub' in payload
    assert payload['sub'] == data['sub']


def test_should_returns_none_when_decode_a_invalid_access_token():
    # arrange
    access_token = 'invalid-access-token'

    # act
    payload = Security.decode_access_token(access_token)

    # assert
    assert payload is None
